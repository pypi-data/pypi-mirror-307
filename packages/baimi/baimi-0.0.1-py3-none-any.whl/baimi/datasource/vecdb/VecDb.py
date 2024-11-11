import logging
import os
import re
from fitxf import DatastoreInterface, DbParams
from fitxf.math.datasource.vecdb.model.ModelDb import ModelDb
from fitxf.math.datasource.vecdb.metadata.Metadata import ModelMetadata
from fitxf import ModelFitTransform
from fitxf import FitXformPca, FitXformCluster, FitXformClusterCosine
from fitxf.math.lang.encode.ImgPt import ImgPt
from fitxf.math.lang.encode.LangModelPtSingleton import LangModelInterface, LangModelPtSingleton
from fitxf.math.lang.encode.LangModelPt import LangModelPt
from fitxf.math.utils import Logging
from fitxf.math.utils.Env import Env


#
# Vector DBs are not yet mature, non-standard query languages, unable to do
# basic DB operations, knowledge in the field hard to find to maintain.
#
# We implement a fast & simple one here, for a single acc/bot id - as a unique
# DB table name.
#
class VecDb(DatastoreInterface):

    LangModelClass = LangModelPt

    MAX_RECORDS = 500000
    MAX_LEN_USER_ID = 64
    # "np" numpy arrays, "torch" Tensors also permitted
    RETURN_TENSORS = 'np'

    def __init__(
            self,
            user_id: str,
            lang: str,
            col_content: str,
            # text, image, sound, video, voice, etc.
            col_content_type: str,
            col_label_user: str,
            col_label_std: str,
            col_embedding: str,
            feature_len: int,
            underlying_db_params: DbParams,
            lm_cache_folder: str = None,
            # Hugging Face language model name, will use some default multilingual model if None
            lm_model_name_or_path: dict = {
                ModelFitTransform.TYPE_TEXT: None,
                ModelFitTransform.TYPE_IMG: None,
            },
            fit_xform_model_name: str = 'cluster',
            cache_tensor_to_file: bool = False,
            file_temp_dir: str = '/tmp',
            # Turn off fitting, thus in plain or test mode
            turn_off_fitting: bool = True,
            logger: Logging = None,
            ignore_warnings: bool = False,
    ):
        self.db_params = underlying_db_params
        if self.db_params.db_type == 'mysql':
            self.db_params.db_create_table_sql = \
                "CREATE TABLE `<TABLENAME>` (\n" + \
                "`" + str(col_content) + "` TEXT NOT NULL,\n" + \
                "`" + str(col_label_user) + "` varchar(255) NOT NULL,\n" + \
                "`" + str(col_label_std) + "` int NOT NULL,\n" + \
                "`" + str(col_embedding) + "` TEXT NOT NULL\n" + \
                ")"
            logger.info('Create table SQL for mysql: ' + str(self.db_params.db_create_table_sql))

        super().__init__(
            db_params = self.db_params,
            logger = logger,
            ignore_warnings = ignore_warnings,
        )
        self.user_id = user_id
        self.lang = lang
        self.col_content = col_content
        self.col_content_type = col_content_type
        self.col_label_user = col_label_user
        self.col_label_standardized = col_label_std
        self.col_embedding = col_embedding
        self.feature_len = feature_len
        self.llm_cache_folder = lm_cache_folder if lm_cache_folder is not None else Env.get_home_download_dir()
        self.llm_model_name_or_path = lm_model_name_or_path
        self.fit_xform_model_name = fit_xform_model_name

        if len(self.user_id) > self.MAX_LEN_USER_ID:
            raise Exception(
                'AccBot ID name too long > ' + str(self.MAX_LEN_USER_ID) + ': "' + str(self.user_id) + '"'
            )

        self.logger.info(
            'Before init, using index id "' + str(user_id) + '", lang "' + str(self.lang)
            + '", content column name "' + str(self.col_content) + '", content type "' + str(self.col_content_type)
            + '", user label "' + str(self.col_label_user)
            + '", label std "' + str(self.col_label_standardized) + '" embedding "' + str(self.col_embedding)
            + '", lm cache folder "' + str(self.llm_cache_folder)
            + '", lm model name or path "' + str(self.llm_model_name_or_path) + '"'
        )

        # Put large tensor objects in persistent object file
        self.cache_tensor_to_file = cache_tensor_to_file
        self.file_temp_dir = file_temp_dir
        self.turn_off_fitting = turn_off_fitting

        self.LangModelClass = {'text': LangModelPt, 'image': ImgPt}
        self.llm_model = {}
        for ctype in self.llm_model_name_or_path.keys():
            self.llm_model[ctype] = self.get_lang_model_class(
                lm_class = self.LangModelClass[ctype],
                llm_cache_folder = self.llm_cache_folder,
                llm_model_name_or_path = self.llm_model_name_or_path[ctype],
            )
            # Model name/path may have changed if we passed in None
            self.llm_model_name_or_path[ctype] = self.llm_model[ctype].get_model_name()
            self.logger.info(
                'Model type "' + str(ctype) + '" initialized with lang "' + str(self.lang)
                + '", lm cache folder "' + str(self.llm_cache_folder)
                + '", lm model name or path "' + str(self.llm_model_name_or_path)
                + '", cache tensor to file "' + str(self.cache_tensor_to_file)
                + '", temp dir "' + str(self.file_temp_dir) + '"'
            )

        self.fixed_tablename_or_index = self.user_id
        self.db_params.db_tablename = self.user_id

        self.logger.info(
            'Using content column name "' + str(self.col_content) + '", user label "' + str(self.col_label_user)
            + '", label std "' + str(self.col_label_standardized) + '" embedding "' + str(self.col_embedding)
            + '", fixed table/index "' + str(self.fixed_tablename_or_index)
            + '", underlying DB params: ' + str(self.db_params.get_db_info())
        )

        self.logger.info('Fit transform model name "' + str(self.fit_xform_model_name) + '"')
        if self.fit_xform_model_name == 'pca':
            self.FitClassObj = FitXformPca(logger=self.logger)
        elif self.fit_xform_model_name == 'cluster':
            self.FitClassObj = FitXformCluster(logger=self.logger)
        elif self.fit_xform_model_name == 'cluster-cosine':
            self.FitClassObj = FitXformClusterCosine(logger=self.logger)
        else:
            raise Exception('Unsupported model "' + str(self.fit_xform_model_name) + '"')

        self.logger.info('Fit transform model class "' + str(type(self.FitClassObj)) + '"')

        self.vec_db_model = ModelFitTransform(
            user_id = self.user_id,
            llm_model = self.llm_model,
            model_db_class = ModelDb,
            model_metadata_class = ModelMetadata,
            col_content = self.col_content,
            col_content_type = col_content_type,
            col_label_user = self.col_label_user,
            col_label_std = self.col_label_standardized,
            col_embedding = self.col_embedding,
            feature_len = self.feature_len,
            numpy_to_b64_for_db = True,
            fit_xform_model = self.FitClassObj,
            cache_tensor_to_file = self.cache_tensor_to_file,
            file_temp_dir = self.file_temp_dir,
            in_plain_or_test_mode = self.turn_off_fitting,
            return_tensors = self.RETURN_TENSORS,
            logger = self.logger,
        )
        self.logger.info(
            'ModelFitTransform initialized successfully for model type "' + str(ctype) + '"'
        )
        return

    def get_lang_model_class(
            self,
            lm_class: type(LangModelInterface),
            llm_cache_folder: str,
            llm_model_name_or_path: dict,
    ) -> LangModelInterface:
        return LangModelPtSingleton.get_singleton(
            LmClass = lm_class,
            cache_folder = llm_cache_folder,
            model_name = llm_model_name_or_path,
            logger = self.logger,
        )

    def get_metadata_table_name(
            self,
    ):
        # lower case to ensure compatibility with DBs such as Opensearch
        return 'metadata'

    def stop_threads(self):
        self.vec_db_model.stop_threads()
        return

    def get_data_length(self):
        return self.vec_db_model.get_data_length()

    # **
    def load_data_model(
            self,
            max_tries = 1,
            background = False,
    ):
        return self.vec_db_model.load_data_model(
            max_tries = max_tries,
            background = background,
        )

    def connect(
            self,
            host     = None,
            port     = None,
            username = None,
            password = None,
            database = None,
            scheme   = None,
            # For our Soprano network, this must be False, otherwise too many problems with CA Authority
            verify_certs = True,
            other_params = None,
    ):
        # already connected upon __init__(), nothing to do
        return

    def get(
            self,
            # e.g. {"answer": "take_seat"}
            match_phrase,
            tablename = None,
            request_timeout = 20,
            params_other = None,
    ):
        if tablename is not None:
            assert tablename == self.fixed_tablename_or_index, str(tablename) + ' != ' + str(self.fixed_tablename_or_index)
        return self.vec_db_model.model_db.underlying_db.get(
            match_phrase = match_phrase,
            tablename = tablename,
            request_timeout = request_timeout,
        )

    def get_all(
            self,
            key = None,
            max_records = 10000,
            tablename_or_index = None,
            return_db_style_records  =True,
            request_timeout = 20,
            params_other = None,
    ):
        if tablename_or_index is not None:
            assert tablename_or_index == self.fixed_tablename_or_index, str(tablename_or_index) + ' != ' + str(self.fixed_tablename_or_index)
        return self.vec_db_model.model_db.underlying_db.get_all(
            key = key,
            max_records = max_records,
            tablename = tablename_or_index,
            request_timeout = request_timeout,
        )

    def get_indexes(self):
        return self.vec_db_model.model_db.underlying_db.get_indexes()

    def delete_index(
            self,
            tablename_or_index,
    ):
        if tablename_or_index is not None:
            assert tablename_or_index == self.fixed_tablename_or_index, str(tablename_or_index) + ' != ' + str(self.fixed_tablename_or_index)
        return self.vec_db_model.model_db.underlying_db.delete_index(
            tablename = tablename_or_index,
        )

    def atomic_delete_add(
            self,
            delete_key: str,
            # list of dicts
            records: list[dict],
            model: str = None,
            params_other = None,
    ):
        return self.vec_db_model.atomic_delete_add(
            delete_key = delete_key,
            records = records,
        )

    def add(
            self,
            # list of dicts
            records,
            model: str = None,
            params_other = None,
    ):
        return self.vec_db_model.add(
            records = records,
        )

    def delete(
            self,
            match_phrase: list[dict],
            tablename_or_index: str = None,
            params_other = None,
    ):
        if tablename_or_index is not None:
            assert tablename_or_index == self.fixed_tablename_or_index, str(tablename_or_index) + ' != ' + str(self.fixed_tablename_or_index)
        match_phrases = match_phrase if type(match_phrase) in [list, tuple] else [match_phrase]

        try:
            return self.vec_db_model.delete(
                match_phrases = match_phrases,
            )
        except Exception as ex:
            self.logger.warning(
                'Error delete from table "' + str(tablename_or_index) + '" match phrases ' + str(match_phrases)
            )

    def cleanup_underlying_db(
            self,
    ):
        try:
            self.vec_db_model.model_db.underlying_db.delete_index(tablename=self.fixed_tablename_or_index)
        except Exception as ex:
            self.logger.error('Error delete DB index "' + str(self.fixed_tablename_or_index) + '": ' + str(ex))
        res = self.vec_db_model.vec_db_metadata.cleanup()
        self.logger.info('Delete result ' + str(res))
        return

    def predict(
            self,
            text_list_or_embeddings,
            content_type = ModelFitTransform.TYPE_TEXT,
            top_k = 5,
            # Instead of just returning the user labels, return full record. Applicable to some models only
            return_full_record = False,
    ):
        return self.vec_db_model.predict(
            text_list_or_embeddings = text_list_or_embeddings,
            content_type = content_type,
            top_k = top_k,
            return_full_record = return_full_record,
        )


if __name__ == '__main__':
    er = Env()
    Env.set_env_vars_from_file(env_filepath=er.REPO_DIR + '/.env.nwae.math.ut')
    lgr = Logging.get_default_logger(log_level=logging.INFO, propagate=False)
    col_content = 'data'
    col_type = 'type'
    col_label_user = 'label'
    col_label_std = 'label_n'
    col_embedding = 'enc'
    vdb = VecDb(
        user_id = 'main_test_vecdb',
        lang = 'en',
        col_content = col_content,
        col_content_type = col_type,
        col_label_user = col_label_user,
        col_label_std = col_label_std,
        col_embedding = col_embedding,
        feature_len = 768,
        lm_cache_folder = er.MODELS_PRETRAINED_DIR,
        fit_xform_model_name = 'cluster',
        # The other info will be auto filled from env var
        underlying_db_params = DbParams(identifier='testvecdb', logger=lgr),
        logger = lgr,
    )
    res = vdb.add(
        records = [
            {col_label_user: 'hola', col_type: 'text', col_content: 'hi'},
            {col_label_user: 'hola', col_type: 'text', col_content: 'hola'},
            {col_label_user: 'hola', col_type: 'text', col_content: 'ohayo'},
            {col_label_user: 'test', col_type: 'text', col_content: 'testing'},
            {col_label_user: 'test', col_type: 'text', col_content: 'cqcq'},
            {col_label_user: 'test', col_type: 'text', col_content: '试试'},
            {col_label_user: 'plov', col_type: 'image', col_content: 'https://img.freepik.com/premium-photo/shakh-plov-cooked-rice-dish-with-raisins-beautiful-plate-islamic-arabic-food_1279579-5074.jpg?w=1800'},
            {col_label_user: 'plov', col_type: 'image', col_content: 'https://img.freepik.com/premium-psd/tasty-fried-vegetable-rice-plate-isolated-transparent-background_927015-3126.jpg?w=1480'},
        ],
    )
    print('add result', res)
    for txt in [
        '안녕', 'привет', '시험하다', 'проверь',
        'https://img.freepik.com/premium-psd/tasty-fried-vegetable-rice-plate-isolated-transparent-background_927015-3126.jpg?w=1480',
    ]:
        content_type = ModelFitTransform.TYPE_IMG if re.match(pattern="^http", string=txt) \
            else ModelFitTransform.TYPE_TEXT
        matches, probs = vdb.predict(
            text_list_or_embeddings = [txt],
            content_type = content_type,
        )
        print('predict result for "' + str(txt) + '"')
        [print(r) for r in list(zip(matches[0], probs[0]))]

    vdb.stop_threads()
    exit(0)
