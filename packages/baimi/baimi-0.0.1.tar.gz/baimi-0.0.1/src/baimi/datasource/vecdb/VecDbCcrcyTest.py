import threading
import logging
import os
import pandas as pd
from fitxf import DbParams
from baimi.datasource.vecdb.VecDb import VecDb
from fitxf.math.utils.Logging import Logging
from fitxf.math.utils.Pandas import Pandas
from fitxf.math.utils.Env import Env


class VecDbCcrcyTest:

    def __init__(
            self,
            test_data_csv_path: str,
            max_records: int,
            user_id: str,
            col_content_type: str,
            col_label: str,
            col_label_number: str,
            col_text: str,
            feature_len: int,
            lm_cache_folder: str,
            logger = None,
    ):
        self.test_data_csv_path = test_data_csv_path
        self.max_records = max_records
        self.user_id = user_id
        self.col_content_type = col_content_type
        self.col_label = col_label
        self.col_label_number = col_label_number
        self.col_text = col_text
        self.col_embedding = 'embedding'
        self.feature_len = feature_len
        self.lm_cache_folder = lm_cache_folder
        self.logger = logger if logger is not None else logging.getLogger()

        self.db_params = DbParams(identifier=str(self.__class__), logger=self.logger)

        # For the purpose of test, make it clear memory very often
        os.environ["VECDB_BG_SLEEP_SECS"] = "1."
        os.environ["VECDB_CLEAR_MEMORY_SECS_INACTIVE"] = "0.5"
        self.vecdb = VecDb(
            user_id = self.user_id,
            lang = 'en',
            col_content = self.col_text,
            col_content_type = self.col_content_type,
            col_label_user = self.col_label,
            col_label_std = self.col_label_number,
            col_embedding = self.col_embedding,
            feature_len = self.feature_len,
            lm_cache_folder = self.lm_cache_folder,
            underlying_db_params = self.db_params,
            fit_xform_model_name = os.environ["VECDB_FIT_XFORM_MODEL"],
            logger = self.logger,
        )
        # clear table from previous tests, if any
        self.vecdb.delete_index(tablename_or_index=user_id)

        Pandas.increase_display()
        df = pd.read_csv(filepath_or_buffer=self.test_data_csv_path, sep=',', index_col=False)
        df[self.col_content_type] = 'text'
        columns_keep = [self.col_content_type, self.col_label, self.col_text]
        df = df[columns_keep]
        df.dropna(inplace=True)
        if len(df) > self.max_records:
            df = df[0:max_records].reset_index(drop=True)

        self.df = df
        # _, _, df[self.col_label_std] = FitUtils().map_labels_to_consecutive_numbers(lbl_list=list(df[self.col_label]))
        self.records = df.to_dict('records')
        self.logger.info('Successfully read data of shape ' + str(self.df.shape))
        self.unique_texts = list(pd.unique(df[self.col_text]))
        self.unique_texts.sort()
        self.logger.info('Unique texts count ' + str(len(self.unique_texts)))
        self.test_stats = {'predict': {}, 'add/delete': {}}
        self.__mutex = threading.Lock()
        # [print(i, txt) for i, txt in enumerate(self.unique_texts)]
        return

    def update_test_stats(self, thread_name, predict_ok=0, add_del_ok=0):
        try:
            self.__mutex.acquire()
            if thread_name not in self.test_stats['predict'].keys():
                self.test_stats['predict'][thread_name] = 0
            if thread_name not in self.test_stats['add/delete'].keys():
                self.test_stats['add/delete'][thread_name] = 0
            self.test_stats['predict'][thread_name] += predict_ok
            self.test_stats['add/delete'][thread_name] += add_del_ok
        finally:
            self.__mutex.release()

    def get_thread_name(self, i):
        thr_name = 't#' + str(i)
        return thr_name

    def test(
            self,
            n_threads: int,
    ):
        threads = {}
        for i in range(n_threads):
            thr_name = self.get_thread_name(i=i)
            threads[i] = threading.Thread(
                target = self.thread_test,
                name = thr_name,
                args = [thr_name],
            )
            threads[i].start()
        for i in range(n_threads):
            threads[i].join()
            self.logger.info('Thread "' + str(self.get_thread_name(i=i)) + '" finished')

        records = self.vecdb.get_all(key=self.col_label, tablename_or_index=self.user_id)
        res_no_embed = [{k:v for k,v in r.items() if k not in [self.col_embedding]} for r in records]
        final_text_list = [r[self.col_text] for r in records]
        df_final = pd.DataFrame(res_no_embed).sort_values(by=[self.col_text], ascending=True)
        print(df_final)
        self.vecdb.stop_threads()

        # Check if all unique inside
        for txt in self.unique_texts:
            assert txt in final_text_list, 'Text "' + str(txt) + '" not in final list of texts ' + str(final_text_list)
        assert len(res_no_embed) == len(self.unique_texts), \
                'Final records count ' + str(len(res_no_embed)) \
                + ' not equal to unique texts ' + str(len(self.unique_texts))
        self.logger.info('VEC DB CONCURRENCY TESTS PASSED')
        print('VEC DB CONCURRENCY TESTS PASSED')
        return

    def thread_test(
            self,
            name: str,
    ):
        self.logger.info('Start thread "' + str(name) + '", records total ' + str(len(self.records)))
        for i, rec in enumerate(self.records):
            # sleep a little
            # time.sleep(np.random.rand()*0.1)
            self.logger.info(
                'Thread "' + str(name) + '" sending record #' + str(i) + ': '
                + str({k:v for k,v in rec.items() if k != self.col_embedding})
            )
            self.logger.info('Thread "' + str(name) + '" sending request #' + str(i) + ': ' + str(rec))
            _ = self.vecdb.atomic_delete_add(
                delete_key = self.col_text,
                records = [rec],
                model = None,
            )
            self.update_test_stats(thread_name=name, add_del_ok=1)
            # _ = self.vecdb.add(records=[rec])
            try:
                top_lbls, _ = self.vecdb.predict(
                    text_list_or_embeddings = [rec[self.col_text]],
                    model = None,
                )
                assert top_lbls[0][0] == rec[self.col_label], \
                    'Predicted top label "' + str(top_lbls[0][0]) + '" not "' + str(rec[self.col_label]) \
                    + '", for text "' + str(rec[self.col_text]) + '"'
                # res_no_embed = [{k: v for k, v in r.items() if k not in [self.col_embedding]} for r in response]
                # self.logger.info('Thread "' + str(name) + '" response #' + str(i) + ': ' + str(response))
                self.update_test_stats(thread_name=name, predict_ok=1)
            except Exception as ex:
                self.logger.error('Error test predict: ' + str(ex))
        return


if __name__ == '__main__':
    evrepo = Env()
    Env.set_env_vars_from_file(env_filepath=evrepo.REPO_DIR + '/env.ut.mysql')
    csv_path = evrepo.NLP_DATASET_DIR + '/lang-model-test/data.csv'
    lgr = Logging.get_logger_from_env_var()
    bot_id = 'bot_vecdb_ccrcy_test'
    col_cont_type = 'type'
    col_label = 'label'
    col_label_number = '__label'
    col_text = 'text'

    VecDbCcrcyTest(
        test_data_csv_path = csv_path,
        max_records = 50,
        user_id = bot_id,
        col_content_type = col_cont_type,
        col_label = col_label,
        col_label_number = col_label_number,
        col_text = col_text,
        feature_len = 384,
        lm_cache_folder = evrepo.MODELS_PRETRAINED_DIR,
        logger = lgr,
    ).test(
        n_threads = 10,
    )
    exit(0)
