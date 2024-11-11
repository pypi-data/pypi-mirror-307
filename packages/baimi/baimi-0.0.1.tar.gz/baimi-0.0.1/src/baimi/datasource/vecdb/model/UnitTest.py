import logging
import time
import uuid
import os
import re
import numpy as np
import pandas as pd
from fitxf import FitXformClusterCosine, FitXformCluster, FitXformPca
from fitxf import DbParams
from fitxf.math.lang.encode.LangModelPtSingleton import LangModelPtSingleton
from fitxf.math.lang.encode.LangModelPt import LangModelPt
from fitxf.math.datasource.vecdb.model.ModelDb import ModelDb
from fitxf.math.datasource.vecdb.metadata.Metadata import ModelMetadata
from fitxf import ModelFitTransform, ModelInterface
# from nwae.math.datasource.vecdb.model.ModelStandard import ModelStandard
from fitxf.math.utils.Logging import Logging
from fitxf.math.utils.Env import Env


class VecDbModelUnitTest:

    COL_CONTENT = 'text'
    COL_LABEL_HUMAN = 'label'
    COL_LABEL_NO = 'label_number'
    COL_EMBEDDING = 'embedding'
    COL_CONTENT_TYPE = 'content_type'

    CLUSTER_TYPES = ['cluster', 'cluster-cosine']

    def __init__(
            self,
            user_id: str,
            model_fit_name: str,
            in_plain_or_test_mode: bool,
            logger = None,
    ):
        self.user_id = user_id
        self.model_fit_name = model_fit_name
        self.in_plain_or_test_mode = in_plain_or_test_mode
        self.logger = logger if logger is not None else Logging.get_default_logger(log_level=logging.INFO, propagate=False)

        os.environ['DB_DEFAULT_TIMEOUT'] = '3'
        self.repo_env = Env()
        self.db_params = DbParams.get_db_params_from_envvars(
            identifier = str(self.__class__),
            db_create_tbl_sql = None,
            db_table = self.user_id,
            verify_certs = os.environ["VERIFY_CERTS"].lower() in ['1', 'true', 'yes'],
        )
        self.lm_cache_folder = self.repo_env.MODELS_PRETRAINED_DIR
        self.file_temp_dir = os.environ["TEMP_DIR"]

        self.sample_txt = [
            'hello world', 'cq cq anyone there', 'privet everyone', 'dobriy dyen', '안녕 你好 привет',
            'rainbow in the sky', 'polka dot bikini', 'white nights', 'aurora northern hemisphere',
            'cold and snowing', 'heating at home', 'thick winter jackets', 'gloves and scarfs',
            # Duplicates
            'cq cq anyone there',
            # Test that won't accidentally delete "hello world"
            'world',
        ]
        self.sample_lbl = [
            'hola', 'hola', 'hola', 'hola', 'hola',
            'color', 'color', 'color', 'color',
            'winter', 'winter', 'winter', 'winter',
            # Duplicates & accidental delete tests
            'hola', 'hola',
        ]
        self.sample_records = pd.DataFrame({
            self.COL_CONTENT: self.sample_txt,
            self.COL_CONTENT_TYPE: ModelInterface.TYPE_TEXT,
            self.COL_LABEL_HUMAN: self.sample_lbl,
        }).to_csv("test_data.csv")# to_dict('records')
        raise Exception('asdf')
        self.len_unique = len(np.unique(self.sample_txt))

        self.partial_train_n = [7, len(self.sample_txt)]
        # duplicates are not removed
        self.partial_train_len_trained_no_remove_dup = [7, len(self.sample_txt)]
        self.partial_train_len_trained_hv_remove_dup = [7, self.len_unique]
        logging.info('Setup unit test data done..')
        return

    def test(
            self,
            cleanup = True,
    ):
        vec_dbs_list = self.__test()
        self.logger.info('Tests executed successfully, now cleaning up...')

        if cleanup:
            self.logger.info('Doing final cleanups...')
            for vdb in vec_dbs_list:
                vdb.stop_threads()
                res = vdb.cleanup()
                self.logger.info('Index(es) removed: ' + str(res))
                try:
                    vdb.model_db.get_underlying_db().delete_index(tablename=self.user_id)
                except:
                    pass
        return

    def __get_vecdb_model(self) -> ModelInterface:
        if self.model_fit_name in ['cluster', 'cluster-cosine', 'pca']:
            Class = ModelFitTransform
            if self.model_fit_name == 'cluster':
                fitxfClass = FitXformCluster
            elif self.model_fit_name == 'cluster-cosine':
                fitxfClass = FitXformClusterCosine
            elif self.model_fit_name == 'pca':
                fitxfClass = FitXformPca
            else:
                fitxfClass = None
        else:
            Class = ModelStandard
            fitxfClass = None
        intent = Class(
            user_id = self.user_id,
            llm_model = {
                ModelInterface.TYPE_TEXT: LangModelPtSingleton.get_singleton(
                    LmClass = LangModelPt,
                    cache_folder = self.lm_cache_folder,
                    logger = self.logger,
                ),
            },
            model_db_class = ModelDb,
            model_metadata_class = ModelMetadata,
            col_content = self.COL_CONTENT,
            col_content_type = self.COL_CONTENT_TYPE,
            col_label_user = self.COL_LABEL_HUMAN,
            col_label_std = self.COL_LABEL_NO,
            col_embedding = self.COL_EMBEDDING,
            feature_len = 0,
            numpy_to_b64_for_db = True,
            fit_xform_model = fitxfClass(logger=self.logger) if fitxfClass is not None else None,
            cache_tensor_to_file = True,
            file_temp_dir = self.file_temp_dir,
            in_plain_or_test_mode = self.in_plain_or_test_mode,
            return_tensors = 'np',
            enable_bg_thread_for_training = False,
            logger = self.logger,
        )
        return intent

    def __test(
            self,
    ):
        test_info = 'DATA CACHE "' + str(self.db_params.get_db_info()) \

        self.vec_model = self.__get_vecdb_model()
        assert self.vec_model.get_data_length() == 0, \
            'Data length not zero at start but ' + str(self.vec_model.get_data_length()) \
            + ' for ' + str(self.db_params.get_db_info())

        i_start = 0
        for round, i_end in enumerate(self.partial_train_n):
            self.logger.info(
                'Train round ' + str(round) + ' range start/end [' + str(i_start) + ', ' + str(i_end) + ']'
            )
            # Delete then add, to remove duplicates previously added
            for r in self.sample_records[i_start:i_end]:
                try:
                    self.vec_model.delete(
                        match_phrases = [{self.COL_CONTENT: r[self.COL_CONTENT]}],
                    )
                except:
                    pass
            self.vec_model.add(
                records = self.sample_records[i_start: i_end],
            )
            # call predict to force update model
            self.vec_model.predict(text_list_or_embeddings=['hi'])
            self.logger.info(
                'Partial train round #' + str(round) + ' Current label maps: ' + str(self.vec_model.map_idx_to_lbl)
                + ', ' + str(self.vec_model.map_lbl_to_idx)
            )

            self.logger.info(
                'Map now: ' + str(self.vec_model.map_idx_to_lbl)
                + ', text labels std ' + str(self.vec_model.text_labels_standardized)
            )
            labels_trained = [
                self.vec_model.map_idx_to_lbl[idx] for idx in self.vec_model.text_labels_standardized
            ]
            self.logger.info(
                'Partial train round #' + str(round) + ' Current text labels trained: ' + str(labels_trained)
            )
            assert len(labels_trained) == self.partial_train_len_trained_hv_remove_dup[round],\
                'Partial train round #' + str(round) + ' trained ' + str(len(labels_trained))\
                + ', expected ' + str(self.partial_train_len_trained_hv_remove_dup[round])
            i_start = i_end

        # Test reload new class
        self.vec_model_2 = self.__get_vecdb_model()
        # assert id(tr) == id(tr_2), 'Singleton class must same but different ' + str(id(tr)) + ' vs ' + str(id(tr_2))
        self.logger.info('Loaded new class from old data for db type "' + str(self.db_params.db_type) + '"')
        assert self.vec_model_2.get_data_length() >= self.len_unique,\
            'Model "' + str(self.model_fit_name) + '". After training data cache type "' + str(self.db_params.db_type)\
            + '", length of encoded text from model load ' + str(len(self.vec_model_2.text_labels_standardized))\
            + ' not expected ' + str(self.len_unique)

        do_full_rec_return = type(self.vec_model) not in [ModelFitTransform]
        if do_full_rec_return:
            pred_full_record, pred_probs_full_record = self.vec_model_2.predict(
                text_list_or_embeddings = self.sample_txt,
                return_full_record = True,
            )
        else:
            pred_full_record, pred_probs_full_record = None, None

        pred_labels, pred_probs = self.vec_model_2.predict(
            text_list_or_embeddings = self.sample_txt,
            return_full_record = False,
        )

        score_accuracy = 0.
        len_sample_txt = len(self.sample_txt)
        for i in range(len_sample_txt):
            s = self.sample_txt[i]
            l = self.sample_lbl[i]
            l_pred = pred_labels[i]
            l_prob = pred_probs[i]
            self.logger.info('For line #' + str(i) + ', predictions: ' + str(l_pred))
            msg = '#' + str(i) + ' Compress model "' + str(type(self.vec_model)) + '", for "' + str(s) \
                  + '", expect "' + str(l) + '", got ' + str(l_pred) + ', probs ' + str(l_prob) + ', ' + test_info
            self.logger.debug(msg)
            try:
                top1_user_label_predicted = l_pred[0]['user_label_estimate']
                top2_user_label_predicted = l_pred[1]['user_label_estimate']
            except:
                top1_user_label_predicted = l_pred[0]
                top2_user_label_predicted = l_pred[1]
            if l != top1_user_label_predicted:
                self.logger.warning(msg)
                # if do_assertion:
                #     assert l == l_pred[0], msg
            score_accuracy += min(1.0*(top1_user_label_predicted == l) + 0.5*(top2_user_label_predicted == l), 1.0)

            if do_full_rec_return:
                l_pred_full_rec = pred_full_record[i]
                l_prob_full_rec = pred_probs_full_record[i]
                msg = '#' + str(i) + ' for "' + str(s) \
                      + '", expect "' + str(l) + '", got ' + str(l_pred_full_rec) + ', probs ' + str(l_prob_full_rec) \
                      + ', ' + str(test_info)
                self.logger.info(msg)
                assert l == l_pred_full_rec[0][self.COL_LABEL_HUMAN], msg
        score_accuracy = score_accuracy / len_sample_txt
        acc_thr = 0.8 if self.model_fit_name in ['cluster', 'cluster-cosine'] else 0.9
        self.logger.info('Model Accuracy for "' + str(self.model_fit_name) + '" ' + str(score_accuracy))
        assert score_accuracy > acc_thr, \
            'Model Accuracy for "' + str(self.model_fit_name) + '" ' + str(score_accuracy) + ' < ' + str(acc_thr)

        #
        # Test delete
        #
        labels_before = [
            self.vec_model.map_idx_to_lbl[idx] for idx in self.vec_model.text_labels_standardized
        ]
        self.logger.info('Before delete, labels trained (' + str(len(labels_before)) + '): ' + str(labels_before))
        for mp in [
            {self.COL_CONTENT: 'world'},
            {self.COL_CONTENT: 'world'},
            {self.COL_CONTENT: 'privet everyone'},
        ]:
            self.vec_model.delete(match_phrases = [mp])
        # call predict to force update model
        self.vec_model.predict(text_list_or_embeddings=['hi'])
        self.logger.info(
            'Before calling predict, data records ' + str([r[self.vec_model.col_content] for r in self.vec_model.data_records])
        )
        labels_after = [
            self.vec_model.map_idx_to_lbl[idx] for idx in self.vec_model.text_labels_standardized
        ]
        # self.logger.info('After delete, labels trained (' + str(len(labels_after)) + '):  ' + str(labels_after))
        assert len(labels_before) - len(labels_after) == 2, \
            'Expected in [0, 2] records deleted from before (' + str(len(labels_before)) + ') ' \
            + str(labels_before) + ', after (' + str(len(labels_after)) + ') ' + str(labels_after)

        # Test sync
        if (self.db_params.db_type != 'memory'):
            # sleep to make sure last update time is no longer the same millisecond when calling predict()
            time.sleep(0.1)
            lbls, probs = self.vec_model.predict(
                text_list_or_embeddings = ['is in sync?'],
                # params_other = {'PCA': self.predict_via_model_compression},
            )
            assert lbls[0][0] != 'sync test', 'Result before sync incorrect ' + str([lbls, probs])
            records_test_sync = [
                {self.COL_LABEL_HUMAN: 'sync test', self.COL_LABEL_NO: 999, self.COL_CONTENT_TYPE: ModelInterface.TYPE_TEXT, self.COL_CONTENT: 'I am in sync'},
                {self.COL_LABEL_HUMAN: 'sync test', self.COL_LABEL_NO: 999, self.COL_CONTENT_TYPE: ModelInterface.TYPE_TEXT, self.COL_CONTENT: 'Are you in sync'},
            ]
            # Despite adding from different object, this action will update DB metadata
            self.vec_model_2.add(
                records = records_test_sync,
            )
            records_before_predict = [r[self.vec_model.col_content] for r in self.vec_model.data_records]
            self.logger.info('Before calling predict, data records ' + str(records_before_predict))

            # despite calling from a different object tr, calling predict() will force checking metadata & model update
            lbls, probs = self.vec_model.predict(
                text_list_or_embeddings = ['is in sync?'],
                top_k = 6,
                # params_other = {'PCA': self.predict_via_model_compression},
            )
            self.logger.info('Prediction of sync test: ' + str(lbls) + ', ' + str(probs))
            try:
                top_label_predicted = lbls[0][0]['user_label_estimate']
            except:
                top_label_predicted = lbls[0][0]

            records_after_predict = [r[self.vec_model.col_content] for r in self.vec_model.data_records]
            diff = list(set(records_after_predict).difference(records_before_predict))
            self.logger.info('After calling predict, data records difference ' + str(diff))
            assert top_label_predicted == 'sync test', \
                'For db type "' + str(self.db_params.db_type) + '", result after sync incorrect ' + str([lbls, probs])

        print('Remaining records: ')
        [print(i, r) for i, r in enumerate(self.vec_model.data_records)]

        self.vec_model.check_model_consistency_with_prev()

        self.logger.info(
            'ALL TESTS PASSED OK (' + test_info + ')'
        )
        return [self.vec_model, self.vec_model_2]


if __name__ == '__main__':
    er = Env()
    Env.set_env_vars_from_file(env_filepath=er.REPO_DIR + '/env.ut.mysql')

    # Put some randomness, so no clashes
    logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False)

    rand_str = re.sub(pattern=".*[\-]", repl="", string=str(uuid.uuid4()))
    bot_unique_id = 'vecdb_model_ut.' + str(rand_str)

    for model, cleanup, plain_mode in [
        # (None, True, False),
        ('pca', True, False),
        ('cluster', True, False),
        ('cluster', True, True),
        ('cluster-cosine', True, False),
    ]:
        for cache_to_file in [False]:
            ut = VecDbModelUnitTest(
                user_id = 'modelut_' + str(model) + '_' + bot_unique_id,
                model_fit_name = model,
                in_plain_or_test_mode = plain_mode,
                logger = logger,
            )
            ut.test(cleanup=cleanup)
            print('TESTS OK FOR cache to file = ' + str(cache_to_file))
    print('ALL TESTS PASSED OK')
    exit(0)
