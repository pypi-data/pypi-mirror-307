import logging
import os
from fitxf import DbParams, ModelInterface
from baimi.datasource.vecdb.VecDb import VecDb
from fitxf.math.utils.Singleton import Singleton
from fitxf.math.utils.Env import Env


class VecDbSingleton:

    @staticmethod
    def get_singleton(
            VecDbClass,    # class type
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
            # Where we cache the language models
            lm_cache_folder: str = None,
            # Language model name, e.g. "xlm-roberta-base", if empty will use default map by language
            lm_model_name_or_path: dict = {
                ModelInterface.TYPE_TEXT: None,
                ModelInterface.TYPE_IMG: None,
            },
            fit_xform_model_name = 'cluster',
            cache_tensor_to_file = False,
            file_temp_dir = '/tmp',
            logger = None,
            ignore_warnings = False,
            return_key = False,
    ) -> VecDb:
        # If these params are different, they will return new object
        db_params = underlying_db_params
        key_id = str(VecDbClass) + '.lang=' + str(lang) + '.model_name=' + str(lm_model_name_or_path) \
                 + '.db_params=' + str(db_params.get_db_info())
        sgt = Singleton(
            class_type = VecDbClass,
            logger     = logger,
        ).get_singleton(
            key_id,
            user_id,
            lang,
            col_content,
            # text, image, sound, video, voice, etc.
            col_content_type,
            col_label_user,
            col_label_std,
            col_embedding,
            feature_len,
            underlying_db_params,
            # Where we cache the language models
            lm_cache_folder,
            # Language model name, e.g. "xlm-roberta-base", if empty will use default map by language
            lm_model_name_or_path,
            fit_xform_model_name,
            cache_tensor_to_file,
            file_temp_dir,
            logger,
            ignore_warnings,
        )
        return (sgt, key_id) if return_key else sgt


class VecDbSingletonUnitTest:
    def __init__(self, logger=None):
        self.logger = logger if logger is not None else logging.getLogger()
        return

    def test(self):
        botid = 'mybot'
        vecdb = VecDbSingleton.get_singleton(
            VecDbClass = VecDb,
            user_id = botid,
            lang = 'multi',
            col_content = 'text',
            col_content_type = 'content_type',
            col_label_user = 'label',
            col_label_std = 'label_number',
            col_embedding = 'embedding',
            feature_len = 384,
            lm_cache_folder = Env().MODELS_PRETRAINED_DIR,
            # lm_model_name_or_path = None,
            fit_xform_model_name = os.environ["VECDB_FIT_XFORM_MODEL"],
            underlying_db_params = DbParams.get_db_params_from_envvars(
                identifier = 'test',
                db_create_tbl_sql = '',
                db_table = botid,
            ),
            cache_tensor_to_file = True,
            logger = self.logger,
        )
        vecdb.stop_threads()
        print('VECDB SINGLETON TESTS OK')
        return


if __name__ == '__main__':
    er = Env()
    Env.set_env_vars_from_file(env_filepath=er.REPO_DIR + '/env.ut.mysql')
    VecDbSingletonUnitTest().test()
    exit(0)
