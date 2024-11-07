import os
import time
import uuid
from typing import Any, Callable, Dict, Generator, List, Optional, Union

from pyspark import SparkConf, SparkContext
from pyspark.rdd import RDD
from pyspark.sql import DataFrame, Row, SparkSession

from dingo.config import GlobalConfig
from dingo.data import Dataset, DataSource, dataset_map, datasource_map
from dingo.exec.base import Executor
from dingo.io import InputArgs, MetaData, ResultInfo, SummaryModel
from dingo.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule
from dingo.utils import log


@Executor.register('spark')
class SparkExecutor(Executor):
    """
    Spark executor
    """

    def __init__(self, input_args: InputArgs,
                 spark_rdd: RDD = None,
                 spark_session: SparkSession = None,
                 spark_conf: SparkConf = None):
        # eval param
        self.model_name = None
        self.model = None
        self.model_type = None
        self.summary: Optional[SummaryModel] = None
        self.bad_info_list: List[ResultInfo] = []
        self.good_info_list: List[ResultInfo] = []

        # init param
        self.input_args = input_args
        self.spark_rdd = spark_rdd
        self.spark_session = spark_session
        self.spark_conf = spark_conf

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['spark_session']
        del state['spark_rdd']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    # def load_data(self) -> Generator[Any, None, None]:
    #     """
    #     Reads data from given path. Returns generator of raw data.
    #
    #     **Run in executor.**
    #
    #     Returns:
    #         Generator[Any, None, None]: Generator of raw data.
    #     """
    #     datasource_cls = datasource_map[self.input_args.datasource]
    #     dataset_cls = dataset_map["spark"]
    #
    #     datasource: DataSource = datasource_cls(input_args=self.input_args)
    #     dataset: Dataset = dataset_cls(source=datasource)
    #     return dataset.get_data()

    def load_data(self) -> RDD:
        return self.spark_rdd

    def execute(self) -> List[SummaryModel]:
        print("============= Init pyspark =============")
        if self.spark_session is not None:
            spark = self.spark_session
            sc = spark.sparkContext
        elif self.spark_conf is not None:
            spark = SparkSession.builder.config(conf=self.spark_conf).getOrCreate()
            sc = spark.sparkContext
        else:
            raise ValueError('[spark_session] and [spark_conf] is none. Please input.')
        print("============== Init Done ===============")

        try:
            # Model init
            model_name = self.input_args.eval_model
            model, model_type = Model.get_model(model_name)
            if model_type == 'llm':
                raise RuntimeError("LLM models are not supported in SparkExecutor yet.")
            self.model_name = model_name
            self.model = model
            self.model_type = model_type

            # Exec Eval
            # if self.spark_rdd is not None:
            #     data_rdd = self.spark_rdd
            # else:
            #     data_rdd = sc.parallelize(self.load_data(), 3)
            data_rdd = self.load_data()
            total = data_rdd.count()

            data_info_list = data_rdd.map(self.evaluate)
            bad_info_list = data_info_list.filter(lambda x: False if len(x['type_list']) == 0 else True)
            bad_info_list.cache()
            self.bad_info_list = bad_info_list
            if self.input_args.save_correct:
                good_info_list = data_info_list.filter(lambda x: False if len(x['type_list']) != 0 else True)
                good_info_list.cache()
                self.good_info_list = good_info_list

            num_bad = bad_info_list.count()
            # calculate count
            self.summary = SummaryModel(
                task_id=str(uuid.uuid1()),
                task_name=self.input_args.task_name,
                eval_model=self.model_name,
                input_path=self.input_args.input_path,
                output_path='',
                create_time=time.strftime('%Y%m%d_%H%M%S', time.localtime()),
                score=0,
                num_good=0,
                num_bad=0,
                total=0,
                type_ratio={m_t: 0 for m_t in Model.rule_metric_type_map},
                name_ratio={}
            )
            self.summary.total = total
            self.summary.num_bad = num_bad
            self.summary.num_good = total - num_bad
            self.summary.score = round(self.summary.num_good / self.summary.total * 100, 2)

            self.summarize()
        except Exception as e:
            raise e
        finally:
            if not self.input_args.save_data:
                self.clean_context_and_session()
            else:
                self.spark_session = spark
        return [self.summary]

    def evaluate(self, data_rdd_item) -> Dict[str, Any]:
        # eval with models ( Big Data Caution ）

        rule_map: List[BaseRule] = self.model
        d: MetaData = data_rdd_item
        result_info = ResultInfo(data_id=d.data_id, prompt=d.prompt, content=d.content)

        log.debug("[RuleMap]: " + str(rule_map))
        if not isinstance(d, MetaData):
            raise TypeError(f'input data must be an instance of MetaData: {str(d)}')

        for r in rule_map:
            rule_name = r.__name__
            # execute rule
            tmp: ModelRes = r.eval(d)
            # analyze result
            if not tmp.error_status:
                continue

            if tmp.type not in result_info.type_list:
                result_info.type_list.append(tmp.type)
            result_info.name_list.append(tmp.type + '-' + rule_name)
            result_info.reason_list.append(tmp.reason)
        return result_info.to_dict()

    def summarize(self):
        # calculate
        for metric_type in Model.rule_metric_type_map:
            num = self.bad_info_list.filter(lambda x: metric_type in x['type_list']).count()
            self.summary.type_ratio[metric_type] = round(num / self.summary.total, 6)

        rule_map = self.model
        for r in rule_map:
            new_name = Model.get_metric_type_by_rule_name(r.__name__) + '-' + r.__name__
            num = self.bad_info_list.filter(lambda x: new_name in x['name_list']).count()
            self.summary.name_ratio[new_name] = round(num / self.summary.total, 6)

        self.summary.type_ratio = dict(sorted(self.summary.type_ratio.items()))
        self.summary.name_ratio = dict(sorted(self.summary.name_ratio.items()))

    def get_summary(self):
        return self.summary

    def get_bad_info_list(self):
        return self.bad_info_list

    def get_good_info_list(self):
        return self.good_info_list

    def save_data(self, start_time):
        output_path = os.path.join(self.input_args.output_path, start_time)
        model_path = os.path.join(output_path, self.model_name)
        if not os.path.exists(model_path):
            os.makedirs(model_path)

    def clean_context_and_session(self):
        self.spark_session.stop()
        self.spark_session.sparkContext.stop()