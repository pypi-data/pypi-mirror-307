import importlib
import os
from functools import wraps
from typing import Callable, Dict, List, Optional

from pydantic import BaseModel

from dingo.config import GlobalConfig
from dingo.model.llm.base import BaseLLM
from dingo.model.rule.base import BaseRule
from dingo.utils import log


class BaseEvalModel(BaseModel):
    name: str
    type: str


class Model:
    """
    Model configuration class.
    """
    module_loaded = False
    rule_metric_type_map = {
        'QUALITY_INEFFECTIVENESS': [],
        'QUALITY_INCOMPLETENESS': [],
        'QUALITY_DISUNDERSTANDABILITY': [],
        'QUALITY_DISSIMILARITY': [],
        'QUALITY_DISFLUENCY': [],
        'QUALITY_IRRELEVANCE': [],
        'QUALITY_INSECURITY': [],
    }
    rule_groups = {}
    rule_name_map = {}
    llm_models = {}

    def __init__(self):
        return

    @classmethod
    def get_model(cls, model_name) -> tuple:
        log.debug(f"[GlobalConfig.config]: {GlobalConfig.config}")
        if model_name in Model.rule_groups:
            log.debug(f"[Load rule model {model_name}]")
            model: List[BaseRule] = Model.rule_groups[model_name]
            model_type = 'rule'
        elif model_name in Model.llm_models:
            log.debug(f"[Load llm model {model_name}]")
            model = Model.llm_models[model_name]
            model_type = 'llm'
        else:
            raise KeyError('no such model: ' + model_name)

        return model, model_type

    @classmethod
    def get_rule_metric_type_map(cls) -> Dict[str, List[Callable]]:
        """
        Returns the rule metric type map.

        Returns:
            Rule metric type map ( { rule_metric_type: [rules] } )
        """
        return cls.rule_metric_type_map

    @classmethod
    def get_rule_group(cls, rule_group_name: str) -> List[Callable]:
        """
        Returns the rule groups by rule_group_name.

        Returns:
            Rule groups ( [rules] ).
        """
        return cls.rule_groups[rule_group_name]

    @classmethod
    def get_rule_groups(cls) -> Dict[str, List[Callable]]:
        """
        Returns the rule groups.

        Returns:
            Rule groups map ( { rule_group_id: [rules] } ).
        """
        return cls.rule_groups

    @classmethod
    def get_rules_by_group(cls, group_name: str) -> List[str]:
        """
        Returns rule by group name.

        Returns:
            Rule name list.
        """
        return [r.metric_type+'-'+r.__name__ for r in Model.get_rule_group(group_name)]

    @classmethod
    def get_rule_by_name(cls, name: str) -> Callable:
        """
        Returns rule by name.

        Returns:
            Rule function.
        """
        return cls.rule_name_map[name]

    @classmethod
    def get_llm_models(cls) -> Dict[str, BaseLLM]:
        """
        Returns the llm models.

        Returns:
            LLM models class List
        """
        return cls.llm_models

    @classmethod
    def get_llm_model(cls, llm_model_name: str) -> BaseLLM:
        """
        Returns the llm model by llm_model_name.
        Args:
            llm_model_name (str): The name of the llm model.

        Returns:
            LLM model class
        """
        return cls.llm_models[llm_model_name]

    @classmethod
    def get_metric_type_by_rule_name(cls, rule_name: str) -> str:
        """
        Returns the metric_type by rule_name.
        Args:
            rule_name (str): The name of the rule.
        Returns:
            metric type.
        """
        rule = cls.rule_name_map[rule_name]
        for metric_type in cls.rule_metric_type_map:
            if rule in cls.rule_metric_type_map[metric_type]:
                return metric_type

    @classmethod
    def print_rule_list(cls) -> None:
        """
        Print the rule list.

        Returns:
            List of rules.
        """
        rule_list = []
        for rule_name in cls.rule_name_map:
            rule_list.append(rule_name)
        print("\n".join(rule_list))

    @classmethod
    def get_all_info(cls):
        """
        Returns rules' map and llm models' map
        """
        raise NotImplementedError()

    @classmethod
    def rule_register(cls, metric_type: str, group: List[str]) -> Callable:
        """
        Register a model. (register)
        Args:
            metric_type (str): The metric type (quality map).
            group (List[str]): The group names.
        """
        def decorator(root_class):
            # group
            for group_name in group:
                if group_name not in cls.rule_groups:
                    cls.rule_groups[group_name] = []
                cls.rule_groups[group_name].append(root_class)
            cls.rule_name_map[root_class.__name__] = root_class

            # metric_type
            if metric_type not in cls.rule_metric_type_map:
                raise KeyError(f'Metric type "{metric_type}" can not be registered.')
            cls.rule_metric_type_map[metric_type].append(root_class)
            root_class.metric_type = metric_type

            @wraps(root_class)
            def wrapped_function(*args, **kwargs):
                return root_class(*args, **kwargs)

            return wrapped_function

        return decorator

    @classmethod
    def llm_register(cls, llm_id: str) -> Callable:
        """
        Register a model. (register)
        Args:
            llm_id (str): Name of llm model class.
        """
        def decorator(root_method):
            cls.llm_models[llm_id] = root_method

            @wraps(root_method)
            def wrapped_function(*args, **kwargs):
                return root_method(*args, **kwargs)

            return wrapped_function

        return decorator


    @classmethod
    def apply_config(cls, custom_config: Optional[str|dict], eval_model: str = ''):
        GlobalConfig.read_config_file(custom_config)
        if GlobalConfig.config and GlobalConfig.config.rule_config:
            for rule, rule_config in GlobalConfig.config.rule_config.items():
                if rule not in cls.rule_name_map:
                    continue
                assert isinstance(rule, str)
                log.debug(f"[Rule config]: config {rule_config} for {rule}")
                cls_rule: BaseRule = cls.rule_name_map[rule]
                config_default = getattr(cls_rule, 'dynamic_config')
                for k,v in rule_config:
                    if v is not None:
                        setattr(config_default, k, v)
                setattr(cls_rule, 'dynamic_config', config_default)
        if GlobalConfig.config and GlobalConfig.config.llm_config:
            for llm, llm_config in GlobalConfig.config.llm_config.items():
                if llm not in cls.llm_models.keys():
                    continue
                assert isinstance(llm, str)
                log.debug(f"[Rule config]: config {llm_config} for {llm}")
                cls_llm: BaseLLM = cls.llm_models[llm]
                config_default = getattr(cls_llm, 'dynamic_config')
                for k,v in llm_config:
                    if v is not None:
                        setattr(config_default, k, v)
                setattr(cls_llm, 'dynamic_config', config_default)
        if GlobalConfig.config and GlobalConfig.config.custom_rule_list:
            model: List[BaseRule] = []

            for rule in GlobalConfig.config.custom_rule_list:
                assert isinstance(rule, str)
                if rule not in Model.rule_name_map:
                    raise KeyError(f"{rule} not in Model.rule_name_map, there are {str(Model.rule_name_map.keys())}")
                model.append(Model.rule_name_map[rule])
            if eval_model in Model.rule_groups:
                raise KeyError(f'eval model: [{eval_model}] already in Model, please input other name.')
            Model.rule_groups[eval_model] = model

    @classmethod
    def load_model(cls):
        if cls.module_loaded:
            return
        this_module_directory = os.path.dirname(os.path.abspath(__file__))
        # rule auto register
        for file in os.listdir(os.path.join(this_module_directory, 'rule')):
            path = os.path.join(this_module_directory, 'rule', file)
            if os.path.isfile(path) and file.endswith('.py') and not file == '__init__.py':
                try:
                    importlib.import_module('dingo.model.rule.' + file.split('.')[0])
                except ModuleNotFoundError as e:
                    log.debug(e)

        # llm auto register
        for file in os.listdir(os.path.join(this_module_directory, 'llm')):
            path = os.path.join(this_module_directory, 'llm', file)
            if os.path.isfile(path) and file.endswith('.py') and not file == '__init__.py':
                try:
                    importlib.import_module('dingo.model.llm.' + file.split('.')[0])
                except ModuleNotFoundError as e:
                    log.debug(e)
                except ImportError as e:
                    log.debug("=" * 30 + " ImportError " + "=" * 30)
                    log.debug(f'module {file.split(".")[0]} not imported because: \n{e}')
                    log.debug("=" * 73)
        cls.module_loaded = True
