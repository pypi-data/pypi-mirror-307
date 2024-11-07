import re

from dingo.config.config import DynamicRuleConfig
from dingo.io import MetaData
from dingo.model.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class XyzShortContent(BaseRule):
    """check whether content is too short."""
    custom_config = DynamicRuleConfig(threshold=20)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from nltk.tokenize import WordPunctTokenizer

        res = ModelRes()
        tk = WordPunctTokenizer()
        tokens = tk.tokenize(input_data.content)
        words = [word for word in tokens if word.isalpha()]
        if len(words) < cls.custom_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = 'Content is too short.'
        return res

@Model.rule_register('QUALITY_IRRELEVANCE', ['xyz_ar'])
class XyzArHeadWord(BaseRule):
    """check whether ar content contains irrelevance tail source info."""

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.xyz_head_word import get_xyz_head_word

        res = ModelRes()
        keyword = get_xyz_head_word("ar")
        content_tail = input_data.content[-100:]
        matches = re.findall("|".join(keyword), content_tail)
        if len(matches) > 0:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = 'Content has irrelevance tail source info.'
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['xyz_ru'])
class XyzRuHeadWord(BaseRule):
    """check whether ru content contains irrelevance tail source info."""

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.xyz_head_word import get_xyz_head_word

        res = ModelRes()
        keyword = get_xyz_head_word("ru")
        content_tail = input_data.content[-100:]
        matches = re.findall("|".join(keyword), content_tail)
        if len(matches) > 0:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = 'Content has irrelevance tail source info.'
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['xyz_ko'])
class XyzKoHeadWord(BaseRule):
    """check whether ko content contains irrelevance tail source info."""

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.xyz_head_word import get_xyz_head_word

        res = ModelRes()
        keyword = get_xyz_head_word("ko")
        content_tail = input_data.content[-100:]
        matches = re.findall("|".join(keyword), content_tail)
        if len(matches) > 0:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = 'Content has irrelevance tail source info.'
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['xyz_th'])
class XyzThHeadWord(BaseRule):
    """check whether th content contains irrelevance tail source info."""

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.xyz_head_word import get_xyz_head_word

        res = ModelRes()
        keyword = get_xyz_head_word("th")
        content_tail = input_data.content[-100:]
        matches = re.findall("|".join(keyword), content_tail)
        if len(matches) > 0:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = 'Content has irrelevance tail source info.'
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['xyz_vi'])
class XyzViHeadWord(BaseRule):
    """check whether vi content contains irrelevance tail source info."""

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.xyz_head_word import get_xyz_head_word

        res = ModelRes()
        keyword = get_xyz_head_word("vi")
        content_tail = input_data.content[-100:]
        matches = re.findall("|".join(keyword), content_tail)
        if len(matches) > 0:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = 'Content has irrelevance tail source info.'
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['xyz_cs'])
class XyzCsHeadWord(BaseRule):
    """check whether cs content contains irrelevance tail source info."""

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.xyz_head_word import get_xyz_head_word

        res = ModelRes()
        keyword = get_xyz_head_word("cs")
        content_tail = input_data.content[-100:]
        matches = re.findall("|".join(keyword), content_tail)
        if len(matches) > 0:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = 'Content has irrelevance tail source info.'
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['xyz_hu'])
class XyzHuHeadWord(BaseRule):
    """check whether hu content contains irrelevance tail source info."""

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.xyz_head_word import get_xyz_head_word

        res = ModelRes()
        keyword = get_xyz_head_word("hu")
        content_tail = input_data.content[-100:]
        matches = re.findall("|".join(keyword), content_tail)
        if len(matches) > 0:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = 'Content has irrelevance tail source info.'
        return res

@Model.rule_register('QUALITY_IRRELEVANCE', ['xyz_sr'])
class XyzSrHeadWord(BaseRule):
    """check whether sr content contains irrelevance tail source info."""

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.xyz_head_word import get_xyz_head_word

        res = ModelRes()
        keyword = get_xyz_head_word("sr")
        content_tail = input_data.content[-100:]
        matches = re.findall("|".join(keyword), content_tail)
        if len(matches) > 0:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = 'Content has irrelevance tail source info.'
        return res