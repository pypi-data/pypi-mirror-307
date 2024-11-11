import logging
import time
import uuid
import os
import re
import numpy as np
import pandas as pd
from inspect import getsourcefile
from fitxf import DbParams, ModelInterface
from baimi.datasource.vecdb.VecDb import VecDb
from fitxf.math.utils.Logging import Logging
from fitxf.math.utils.Env import Env

ClassifyClass = VecDb


class VecDbUnitTest:

    COL_CONTENT = 'text'
    COL_CONTENT_TYPE = 'type'
    COL_LABEL_HUMAN = 'label'
    COL_LABEL_NO = 'label_number'
    COL_EMBEDDING = 'embedding'

    CLUSTER_TYPES = ['cluster', 'cluster-cosine']

    def __init__(
            self,
            user_id,
            db_params,
            lm_cache_folder,
            lm_model_name_or_path,
            model_cache_folder,
            is_db_exist,
            cache_tensor_to_file = False,
            file_temp_dir = '/tmp',
            turn_off_fitting = False,
            vdb_model = None,
            logger = None,
    ):
        self.user_id = user_id
        self.db_params = db_params
        self.lm_cache_folder = lm_cache_folder
        self.lm_model_name_or_path = lm_model_name_or_path
        self.model_cache_folder = model_cache_folder
        self.is_db_exist = is_db_exist
        self.vdb_model = vdb_model
        self.cache_tensor_to_file = cache_tensor_to_file
        self.file_temp_dir = file_temp_dir
        self.turn_off_fitting = turn_off_fitting
        self.logger = logger

        os.environ['DB_DEFAULT_TIMEOUT'] = '3'

        self.lang = 'en'
        path = os.path.abspath(getsourcefile(lambda: 0))
        path_folder = os.path.dirname(path)
        self.sample_records_df = pd.read_csv(path_folder + "/test_vecdb.csv")
        self.sample_records = self.sample_records_df.to_dict('records')
        self.sample_txt = list(self.sample_records_df[self.COL_CONTENT])
        self.sample_lbl = list(self.sample_records_df[self.COL_LABEL_HUMAN])

        self.len_unique = len(np.unique(self.sample_records_df[self.COL_CONTENT]))

        self.partial_train_n = [7, len(self.sample_records)]
        # duplicates are not removed
        self.partial_train_len_trained_no_remove_dup = [7, len(self.sample_records)]
        self.partial_train_len_trained_hv_remove_dup = [7, self.len_unique]
        logging.info('Setup unit test data done..')

    def test(
            self,
            use_add_delete = False,
            params_train = None,
            do_assertion = True,
    ):
        vec_dbs_list = self.__test(
            use_add_delete = use_add_delete,
            params_train = params_train,
            do_assertion = do_assertion,
        )
        self.logger.info('Tests executed successfully, now cleaning up...')

        self.logger.info('Doing final cleanups...')
        for vdb in vec_dbs_list:
            res = vdb.cleanup_underlying_db()
            self.logger.info('Index(es) removed: ' + str(res))
            vdb.stop_threads()
        return

    def __get_intent_singleton(self) -> VecDb:
        # For the purpose of test, make it clear memory very often
        os.environ["VECDB_BG_SLEEP_SECS"] = "0.1"
        os.environ["VECDB_CLEAR_MEMORY_SECS_INACTIVE"] = "0.001"
        intent = ClassifyClass(
            user_id = self.user_id,
            lang = self.lang,
            col_content = self.COL_CONTENT,
            col_content_type = self.COL_CONTENT_TYPE,
            col_label_user = self.COL_LABEL_HUMAN,
            col_label_std = self.COL_LABEL_NO,
            col_embedding = self.COL_EMBEDDING,
            feature_len = 768,
            lm_cache_folder = self.lm_cache_folder,
            lm_model_name_or_path = {
                ModelInterface.TYPE_TEXT: self.lm_model_name_or_path,
                ModelInterface.TYPE_IMG: None,
            },
            fit_xform_model_name = self.vdb_model,
            underlying_db_params = self.db_params,
            cache_tensor_to_file = self.cache_tensor_to_file,
            file_temp_dir = self.file_temp_dir,
            turn_off_fitting = self.turn_off_fitting,
            logger = self.logger,
        )
        return intent

    def __test(
            self,
            use_add_delete = False,
            params_train = None,
            do_assertion = True,
    ):
        params_train = {} if params_train is None else params_train

        test_info = 'DATA CACHE "' + str(self.db_params.get_db_info()) \
                    + '", ADD/DELETE INSTEAD OF TRAIN=' + str(use_add_delete) + ')'

        ClassifyClass.MODEL_COMPRESSION_SLEEP_SECS = 0.5

        tr = self.__get_intent_singleton()
        self.vec_db = tr
        tr.cleanup_underlying_db()
        self.logger.info('Model lengths after clearing DB at start = ' + str(tr.get_data_length()))
        assert tr.get_data_length() == 0, \
                'Data length not zero at start but ' + str(tr.get_data_length()) + ' for ' + str(self.db_params.get_db_info())

        i_start = 0
        for round, i_end in enumerate(self.partial_train_n):
            self.logger.info(
                'Train round ' + str(round) + ' range start/end [' + str(i_start) + ', ' + str(i_end)
                + '], params train: ' + str(params_train) + ', use add/delete ' + str(use_add_delete)
            )
            # Delete then add, to remove duplicates previously added
            for r in self.sample_records[i_start:i_end]:
                # Only do delete after first round, so that table/etc already created
                if round > 0:
                    tr.delete(
                        match_phrase = [{self.COL_CONTENT: r[self.COL_CONTENT]}],
                    )
            tr.add(
                records = self.sample_records[i_start: i_end],
                model = None,
            )
            # call predict to force update model
            tr.predict(text_list_or_embeddings=['hi'])
            self.logger.info(
                'Partial train round #' + str(round) + ' Current label maps: ' + str(tr.vec_db_model.map_idx_to_lbl)
                + ', ' + str(tr.vec_db_model.map_lbl_to_idx)
            )

            self.logger.info(
                'Map now: ' + str(tr.vec_db_model.map_idx_to_lbl)
                + ', text labels std ' + str(tr.vec_db_model.text_labels_standardized)
            )
            labels_trained = [
                tr.vec_db_model.map_idx_to_lbl[idx] for idx in tr.vec_db_model.text_labels_standardized
            ]
            self.logger.info(
                'Partial train round #' + str(round) + ' Current text labels trained: ' + str(labels_trained)
            )
            assert len(labels_trained) == self.partial_train_len_trained_hv_remove_dup[round],\
                'Partial train round #' + str(round) + ' trained ' + str(len(labels_trained))\
                + ', expected ' + str(self.partial_train_len_trained_hv_remove_dup[round])
            i_start = i_end

        if (self.db_params.db_type == 'memory'):
            # For memory type, without model files, it will have nothing if instantiate new class, so cannot do that
            tr_2 = tr
        else:
            # Test reload new class
            tr_2 = self.__get_intent_singleton()
            # assert id(tr) == id(tr_2), 'Singleton class must same but different ' + str(id(tr)) + ' vs ' + str(id(tr_2))
            self.logger.info('Loaded new class from old data for db type "' + str(self.db_params.db_type) + '"')
        self.vec_db_2 = tr_2
        assert tr_2.get_data_length() >= self.len_unique,\
            'After training data cache type "' + str(db_params.db_type)\
            + '", length of encoded text from model load ' + str(len(tr_2.vec_db_model.text_labels_standardized))\
            + ' not expected ' + str(self.len_unique)

        do_full_rec_return = self.vdb_model not in self.CLUSTER_TYPES
        if do_full_rec_return:
            pred_full_record, pred_probs_full_record = tr_2.predict(
                text_list_or_embeddings = self.sample_txt,
                return_full_record = True,
            )
        else:
            pred_full_record, pred_probs_full_record = None, None

        pred_labels, pred_probs = tr_2.predict(
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
            msg = '#' + str(i) + ' Compress model "' + str(self.vdb_model) + '", for "' + str(s) \
                  + '", expect "' + str(l) + '", got ' + str(l_pred) + ', probs ' + str(l_prob) + ', ' + test_info
            self.logger.info(msg)
            top1_user_label_predicted \
                = l_pred[0]['user_label_estimate'] if self.vdb_model in self.CLUSTER_TYPES else l_pred[0]
            top2_user_label_predicted \
                = l_pred[1]['user_label_estimate'] if self.vdb_model in self.CLUSTER_TYPES else l_pred[1]
            if l != top1_user_label_predicted:
                self.logger.warning(msg)
                # if do_assertion:
                #     assert l == l_pred[0], msg
            score_accuracy += min(1.0*(top1_user_label_predicted == l) + 0.5*(top2_user_label_predicted == l), 1.0)

            if do_full_rec_return:
                l_pred_full_rec = pred_full_record[i]
                l_prob_full_rec = pred_probs_full_record[i]
                msg = '#' + str(i) + ' Compress model "' + str(self.vdb_model) + '", for "' + str(s) \
                      + '", expect "' + str(l) + '", got ' + str(l_pred_full_rec) + ', probs ' + str(l_prob_full_rec) \
                      + ', ' + str(test_info)
                self.logger.info(msg)
                # raise Exception('asdf')
                if do_assertion:
                    assert l == l_pred_full_rec[0][self.COL_LABEL_HUMAN], msg
        score_accuracy = score_accuracy / len_sample_txt
        acc_thr = 0.85
        assert score_accuracy > acc_thr, \
            'Compress model "' + str(self.vdb_model) + ' accuracy ' + str(score_accuracy) + ' < ' + str(acc_thr)

        #
        # Test delete
        #
        labels_before = [
            tr.vec_db_model.map_idx_to_lbl[idx] for idx in tr.vec_db_model.text_labels_standardized
        ]
        self.logger.info('Before delete, labels trained (' + str(len(labels_before)) + '): ' + str(labels_before))
        for mp in [
            {self.COL_CONTENT: 'world'},
            {self.COL_CONTENT: 'world'},
            {self.COL_CONTENT: 'privet everyone'},
            {self.COL_CONTENT_TYPE: ModelInterface.TYPE_IMG, self.COL_CONTENT: 'https://assets.teenvogue.com/photos/66f2dbe59926099a9dec34ce/16:9/w_2240,c_limit/2173404736'},
        ]:
            try:
                tr.delete(match_phrase = [mp])
            except Exception as ex_del:
                self.logger.info('Delete error for match phrase ' + str(mp) + ': ' + str(ex_del))
        # call predict to force update model
        tr.predict(text_list_or_embeddings=['hi'])
        self.logger.info(
            'Before calling predict, data records ' + str([r[tr_2.col_content] for r in tr_2.vec_db_model.data_records])
        )
        labels_after = [
            tr.vec_db_model.map_idx_to_lbl[idx] for idx in tr.vec_db_model.text_labels_standardized
        ]
        # self.logger.info('After delete, labels trained (' + str(len(labels_after)) + '):  ' + str(labels_after))
        assert len(labels_before) - len(labels_after) == 2, \
            'Expected in [0, 2] records deleted from before (' + str(len(labels_before)) + ') ' \
            + str(labels_before) + ', after (' + str(len(labels_after)) + ') ' + str(labels_after)

        # Test sync
        if (self.db_params.db_type != 'memory'):
            # sleep to make sure last update time is no longer the same millisecond when calling predict()
            time.sleep(0.1)
            lbls, probs = tr.predict(
                text_list_or_embeddings = ['is in sync?'],
                # params_other = {'PCA': self.predict_via_model_compression},
            )
            assert lbls[0][0] != 'sync test', 'Result before sync incorrect ' + str([lbls, probs])
            records_test_sync = [
                {self.COL_LABEL_HUMAN: 'sync test', self.COL_LABEL_NO: 999, self.COL_CONTENT_TYPE: 'text', self.COL_CONTENT: 'I am in sync'},
                {self.COL_LABEL_HUMAN: 'sync test', self.COL_LABEL_NO: 999, self.COL_CONTENT_TYPE: 'text', self.COL_CONTENT: 'Are you in sync'},
            ]
            # Despite adding from different object, this action will update DB metadata
            tr_2.add(
                records = records_test_sync,
            )
            records_before_predict = [r[tr_2.col_content] for r in tr.vec_db_model.data_records]
            self.logger.info('Before calling predict, data records ' + str(records_before_predict))

            # despite calling from a different object tr, calling predict() will force checking metadata & model update
            lbls, probs = tr_2.predict(
                text_list_or_embeddings = ['is in sync?'],
                top_k = 6,
                # params_other = {'PCA': self.predict_via_model_compression},
            )
            self.logger.info('Prediction of sync test: ' + str(lbls) + ', ' + str(probs))
            top_label_predicted = \
                lbls[0][0]['user_label_estimate'] if self.vdb_model in self.CLUSTER_TYPES else lbls[0][0]

            records_after_predict = [r[tr_2.col_content] for r in tr.vec_db_model.data_records]
            diff = list(set(records_after_predict).difference(records_before_predict))
            self.logger.info('After calling predict, data records difference ' + str(diff))
            assert top_label_predicted == 'sync test', \
                'For db type "' + str(self.db_params.db_type) + '", model predict = "' \
                + str(self.vdb_model) + '", result after sync incorrect ' + str([lbls, probs])

        print('Remaining records: ')
        [print(i, r) for i, r in enumerate(tr.vec_db_model.data_records)]

        tr.vec_db_model.check_model_consistency_with_prev()

        self.logger.info(
            'ALL TESTS PASSED OK (' + test_info + ')'
        )
        return [tr, tr_2]


if __name__ == '__main__':
    UnitTestClass = VecDbUnitTest
    lgr = Logging.get_default_logger(log_level=logging.INFO, propagate=False)
    er = Env(logger=lgr)
    Env.set_env_vars_from_file(env_filepath=er.REPO_DIR + '/env.ut.mysql')

    rand_str = re.sub(pattern=".*[\-]", repl="", string=str(uuid.uuid4()))
    bot_unique_id = 'bot_intent_unit_test_data_index.' + str(rand_str)

    cache_tensor_to_file = True
    db_params = DbParams(
        identifier = str(UnitTestClass),
        logger = lgr,
    )

    ut = UnitTestClass(
        user_id = bot_unique_id,
        db_params = db_params,
        lm_cache_folder = er.MODELS_PRETRAINED_DIR,
        lm_model_name_or_path = None,
        model_cache_folder = None,
        is_db_exist = True,
        vdb_model = os.environ["VECDB_FIT_XFORM_MODEL"],
        cache_tensor_to_file = cache_tensor_to_file,
        file_temp_dir = ".",
        turn_off_fitting = str(os.environ["VECDB_FIT_XFORM_MODEL_TEST_MODE"]).lower() in ['1', 'yes', 'true'],
        logger = lgr,
    )
    ut.test()
    print('TESTS OK FOR cache to file = ' + str(cache_tensor_to_file))
    print('ALL TESTS PASSED OK')
    exit(0)
