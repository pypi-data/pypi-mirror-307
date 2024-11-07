import re
import string

from dingo.config.config import DynamicRuleConfig
from dingo.io import MetaData
from dingo.model.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['text_base_all'])
class QaContentShort(BaseRule):
    dynamic_config = DynamicRuleConfig(threshold = 20)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content.encode('utf-8')
        if len(content) <= cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = 'Content is too short.'
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaOnlyUrl(BaseRule):
    """check whether content is only an url link."""
    dynamic_config = DynamicRuleConfig(pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        SEARCH_REGEX = re.compile(cls.dynamic_config.pattern)
        content_without_url = SEARCH_REGEX.sub("", input_data.content)
        if len(content_without_url.strip()) == 0:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = 'Content is only an url link.'
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', [])
class QaChaosEnLine(BaseRule):
    """check whether content has english garbled characters at the line level."""
    dynamic_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        import jieba

        from dingo.model.rule.common.detect_lang import decide_language_by_str
        from dingo.model.rule.common.util import delete_punc_ch, delete_punc_en

        res = ModelRes()
        content = input_data.content

        language = decide_language_by_str(content)
        if language != 'en':
            return res
        for content_line in content.split("\n"):
            if len(content_line.strip()) == 0:
                continue
            af_en = delete_punc_en(content_line)
            af_ch = delete_punc_ch(af_en)
            str_len = len(af_ch)
            seg_len = len(list(jieba.cut(af_ch)))
            if seg_len == 0:
                continue
            if str_len / seg_len < 1.2:
                res.error_status = True
                res.type = 'QUALITY_INEFFECTIVENESS'
                res.name = cls.__name__
                res.reason = content_line
                return res
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', [])
class QaChaosZh(BaseRule):
    """check whether content has chinese garbled characters."""
    dynamic_config = DynamicRuleConfig(pattern = r'[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+(""|[\n\s])')

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        import jieba
        from hanziconv import HanziConv

        from dingo.model.rule.common.detect_lang import decide_language_by_str
        from dingo.model.rule.common.util import delete_punc_ch, delete_punc_en, get_tokens

        res = ModelRes()
        content = input_data.content

        language = decide_language_by_str(content)
        if language != 'zh':
            return res
        af_en = delete_punc_en(content)
        af_ch = delete_punc_ch(af_en)
        text = re.sub(cls.dynamic_config.pattern, "", af_ch)
        simplified_text = HanziConv.toSimplified(text)
        seg_len = len(list(jieba.cut(simplified_text)))
        str_len = len(text)
        if str_len == 0 or seg_len == 0 and get_tokens(content, language) < 50:
            return res
        if str_len / seg_len > 1.2:
            return res
        else:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = 'Content has chinese garbled characters.'
            return res
        return res


@Model.rule_register('QUALITY_DISUNDERSTANDABILITY', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaEnterMore(BaseRule):
    """check whether content has 8 consecutive carriage returns."""
    dynamic_config = DynamicRuleConfig(key_list=[r"\n{8,}", r"\r\n{8,}"])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        for p in cls.dynamic_config.key_list:
            SEARCH_REGEX = re.compile(p)
            match = SEARCH_REGEX.search(content)
            if match:
                res.error_status = True
                res.type = 'QUALITY_DISUNDERSTANDABILITY'
                res.name = cls.__name__
                res.reason = 'Content has 8 consecutive carriage returns.'
                return res
        return res


@Model.rule_register('QUALITY_DISUNDERSTANDABILITY', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaSpaceMore(BaseRule):
    """check whether content has 500 spaces."""
    dynamic_config = DynamicRuleConfig(pattern=" {500,}")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        SEARCH_REGEX = re.compile(cls.dynamic_config.pattern)
        match = SEARCH_REGEX.search(content)
        if match:
            res.error_status = True
            res.type = 'QUALITY_DISUNDERSTANDABILITY'
            res.name = cls.__name__
            res.reason = 'Content has 500 spaces.'
            return res
        return res


@Model.rule_register('QUALITY_DISUNDERSTANDABILITY', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaEnterRatioMore(BaseRule):
    """check whether the number of enter / the number of content > 25%"""
    dynamic_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        if len(content) == 0:
            return res

        ratio = content.count("\n") / len(content)
        if ratio > 0.25:
            res.error_status = True
            res.type = 'QUALITY_DISUNDERSTANDABILITY'
            res.name = cls.__name__
            res.reason = 'The number of enter / the number of content > 25%.'
            return res
        return res


@Model.rule_register('QUALITY_DISFLUENCY', ['text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaWordStuck(BaseRule):
    """check whether words are stuck."""
    dynamic_config = DynamicRuleConfig(
        key_list=[
            r"https?://[^\s]+|www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            r"\.pdf$",
            r"\w+\.bat",
            r"(\/.*\/.*)",
            r"[01]+|[0-7]+|0x[0-9a-fA-F]+"
        ]
    )

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        import wordninja

        from dingo.model.rule.common.detect_lang import decide_language_by_str
        from dingo.model.rule.common.util import is_sha256

        res = ModelRes()
        content = input_data.content
        language = decide_language_by_str(content)
        if language != 'en':
            return res

        for p in cls.dynamic_config.key_list:
            content = re.sub(p, "", content)
        word_list = [
            word.strip(string.punctuation) for word in
            re.split(r"[⁃>#%-.—,–!?;:\s|_/   =\\@\((.*?)\)\[(.*?)\]]\s*", content)
        ]
        for longest_string in word_list:
            if len(longest_string) > 45 and is_sha256(longest_string) == False:
                lan = decide_language_by_str(longest_string)
                cut = wordninja.split(longest_string)
                if lan == "en" and len(cut) > 1:
                    res.error_status = True
                    res.type = 'QUALITY_DISFLUENCY'
                    res.name = cls.__name__
                    res.reason = str(longest_string)
                    return res
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaHtmlTag(BaseRule):
    """check whether content has image links or html tags."""
    dynamic_config = DynamicRuleConfig(pattern=r"(<img[^>]*>)|<p[^>]*>(.*?)<\/p>|<o:p[^>]*>(.*?)<\/o:p>")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        matches = re.search(cls.dynamic_config.pattern, content)
        if matches:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = matches.group()
            return res
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class QaInvisibleChar(BaseRule):
    """check whether content has invisible chars."""
    dynamic_config = DynamicRuleConfig(pattern=r"[\u2000-\u200F\u202F\u205F\u3000\uFEFF\u00A0\u2060-\u206F\uFEFF\xa0]")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        matches = re.findall(cls.dynamic_config.pattern, content)
        if matches:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = list(set(matches))
            return res
        return res

@Model.rule_register('QUALITY_DISFLUENCY', ['pdf_all'])
class QaCharSplit(BaseRule):
    """check pdf content char split."""
    dynamic_config = DynamicRuleConfig(pattern=r"(?:(?:[a-zA-Z]\s){5}[a-zA-Z])", threshold=3)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        matches = re.findall(cls.dynamic_config.pattern, content)
        count = len(matches)
        if count >= cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_DISFLUENCY'
            res.name = cls.__name__
            res.reason = ','.join(matches)
            return res
        return res

@Model.rule_register('QUALITY_DISFLUENCY', ['pdf_all'])
class QaAbnormalNumber(BaseRule):
    """check pdf content abnormal book page or index number."""
    dynamic_config = DynamicRuleConfig(pattern=r'\n{4}\d+\n{4}')

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        match = re.search(cls.dynamic_config.pattern, content)
        if match:
            res.error_status = True
            res.type = 'QUALITY_DISFLUENCY'
            res.name = cls.__name__
            res.reason = match.group(0).strip("\n")
            return res
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['pdf_all'])
class QaLatexSpecialChar(BaseRule):
    """check pdf content latex abnormal char."""
    dynamic_config = DynamicRuleConfig(pattern=r'\$\$(.*?\!\!.*?)\$\$')

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        match = re.search(cls.dynamic_config.pattern, content)
        if match:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = match.group(0).strip("\n")
            return res
        return res


@Model.rule_register('QUALITY_DISFLUENCY', ['pdf_all'])
class QaWordSplit(BaseRule):
    """check pdf word abnormal split such as "ca- se"."""
    dynamic_config = DynamicRuleConfig(pattern=r'[A-Za-z]+-\s*$')

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        match = re.findall(cls.dynamic_config.pattern, content)
        if match:
            res.error_status = True
            res.type = 'QUALITY_DISFLUENCY'
            res.name = cls.__name__
            res.reason = ','.join(match)
            return res
        return res


if __name__ == '__main__':
    data = MetaData(
        data_id = '',
        prompt = '',
        content = "<img>你好<p>苹果</p>"
    )
    tmp = QaContentShort().eval(data)
    print(tmp)

