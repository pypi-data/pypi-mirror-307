import re
from typing import Tuple

from dingo.config.config import DynamicRuleConfig
from dingo.io import MetaData
from dingo.model.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.rule.base import BaseRule


@Model.rule_register("QUALITY_INEFFECTIVENESS", ['pretrain'])
class CommonAlphaWords(BaseRule):
    """check whether the ratio of words that contain at least one alphabetic character > 0.6 """
    dynamic_config = DynamicRuleConfig(threshold=0.6)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from nltk.tokenize import word_tokenize

        from dingo.model.rule.common.detect_lang import decide_language_by_str

        res = ModelRes()
        content = input_data.content
        language = decide_language_by_str(content)
        if language != 'en':
            return res
        words = word_tokenize(content)
        n_words = len(words)
        if n_words == 0:
            return res

        n_alpha_words = sum([any((c.isalpha() for c in w)) for w in words])
        ratio = n_alpha_words / n_words
        if ratio > cls.dynamic_config.threshold:
            pass
        else:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = "The ratio of words that contain at least one alphabetic character is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_DISUNDERSTANDABILITY", ['pretrain'])
class CommonCapitalWords(BaseRule):
    """check whether capital words ratio > 0.2"""
    dynamic_config = DynamicRuleConfig(threshold=0.2)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from nltk.tokenize import WordPunctTokenizer

        res = ModelRes()
        content = input_data.content
        words = WordPunctTokenizer().tokenize(content)
        num_words = len(words)
        num_caps_words = sum(map(str.isupper, words))
        ratio = num_caps_words / num_words
        if ratio > cls.dynamic_config.threshold and num_words < 200:
            res.error_status = True
            res.type = 'QUALITY_DISUNDERSTANDABILITY'
            res.name = cls.__name__
            res.reason = 'ratio: '+ str(ratio)
            return res
        return res


@Model.rule_register("QUALITY_INEFFECTIVENESS", ['pretrain'])
class CommonCharNumber(BaseRule):
    """check whether the number of char > 100 """
    dynamic_config = DynamicRuleConfig(threshold = 100)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        text = input_data.content
        text = text.strip()
        text = text.replace(" ", "")
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        num_char = len(text)
        if num_char < cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = "The number of char is: " + str(num_char)
        return res


@Model.rule_register('QUALITY_INCOMPLETENESS', ['default','sft','pretrain','benchmark','llm_base', 'text_base_all'])
class CommonColonEnd(BaseRule):
    """check whether the last char is ':'"""
    dynamic_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content
        if len(content) <= 0:
            return res
        if content[-1] == ':':
            res.error_status = True
            res.type = 'QUALITY_INCOMPLETENESS'
            res.name = cls.__name__
            res.reason = content[-100:]
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['default','sft','pretrain','benchmark','text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonContentNull(BaseRule):
    """check whether content is null"""
    dynamic_config = DynamicRuleConfig()

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        count = len(input_data.content.strip())
        if count == 0:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = 'Content is empty.'
        return res


@Model.rule_register("QUALITY_DISUNDERSTANDABILITY", [])
class CommonCurlyBracket(BaseRule):
    """check whether the ratio of the number of {,} and the number of characters < 0.025"""
    dynamic_config = DynamicRuleConfig(threshold=0.025)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        num = content.count('{') + content.count('}')
        ratio = num / len(content) if len(content) !=0 else 0
        if ratio > cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_DISUNDERSTANDABILITY'
            res.name = cls.__name__
            res.reason = 'The ratio of curly bracket and characters is : ' + str(ratio)
        return res


@Model.rule_register('QUALITY_DISSIMILARITY', ['default','sft','pretrain','benchmark','text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonDocRepeat(BaseRule):
    """check whether content repeats"""
    dynamic_config = DynamicRuleConfig(threshold=80)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import base_rps_frac_chars_in_dupe_ngrams

        res = ModelRes()
        repeat_score = base_rps_frac_chars_in_dupe_ngrams(6, input_data.content)
        if repeat_score >= cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_DISSIMILARITY'
            res.name = cls.__name__
            res.reason = 'Repeatability of text is too high, with ratio： ' + str(repeat_score)
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['default','sft','pretrain','benchmark','text_base_all','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonHtmlEntity(BaseRule):
    """check whether content has html entity"""
    dynamic_config = DynamicRuleConfig(key_list=[
        "nbsp",
        "lt",
        "gt",
        "amp",
        "quot",
        "apos",
        "hellip",
        "ndash",
        "mdash",
        "lsquo",
        "rsquo",
        "ldquo",
        "rdquo",
    ])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        entities = cls.dynamic_config.key_list
        full_entities_1 = [f"&{entity}；" for entity in entities]
        full_entities_2 = [f"&{entity};" for entity in entities]
        full_entities_3 = [f"＆{entity};" for entity in entities]
        full_entities_4 = [f"＆{entity}；" for entity in entities]
        full_entities = full_entities_1 + full_entities_2 + full_entities_3 + full_entities_4
        # half_entity_1 = [f"{entity}；" for entity in entities]
        half_entity_2 = [f"＆{entity}" for entity in entities]
        half_entity_3 = [f"&{entity}" for entity in entities]
        # half_entity_4 = [f"{entity};" for entity in entities]
        half_entities = half_entity_2 + half_entity_3
        # maked_entities = [f"{entity}" for entity in entities]
        all_entities = full_entities + half_entities

        error_entity = []
        for entity in all_entities:
            if entity in content:
                res.error_status = True
                res.type = 'QUALITY_IRRELEVANCE'
                res.name = cls.__name__
                error_entity.append(entity)
        if len(error_entity) != 0:
            res.reason = list(set(error_entity))
        return res


@Model.rule_register('QUALITY_INSECURITY', ['default','pretrain','benchmark'])
class CommonIDCard(BaseRule):
    """check if the content contains ID card. """
    dynamic_config = DynamicRuleConfig(pattern = r"(身\s{0,10}份|id\s{0,10}number\s{0,10}|identification|identity|\s{0,10}ID\s{0,10}No\s{0,10}|id\s{0,10}card\s{0,10}|NRIC\s{0,10}number\s{0,10}|IC\s{0,10}number\s{0,10}|resident\s{0,10}registration\s{0,10}|I.D.\s{0,10}Number\s{0,10})")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import Extractor

        res = ModelRes()
        match = re.search(cls.dynamic_config.pattern, input_data.content, re.I)
        if match:
            person_id = Extractor().extract_id_card(input_data.content)
            if len(person_id) != 0:
                res.error_status = True
                res.type = 'QUALITY_INSECURITY'
                res.name = cls.__name__
                res.reason = str(person_id)
        return res


@Model.rule_register("QUALITY_INCOMPLETENESS", ['pretrain','benchmark'])
class CommonLineEndWithEllipsis(BaseRule):
    """check whether the ratio of line ends with ellipsis < 0.3 """
    dynamic_config = DynamicRuleConfig(threshold=0.3, key_list = ["...", "…"])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import TextSlice, split_paragraphs

        res = ModelRes()
        raw_content = input_data.content
        raw_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=lambda x: x, remove_empty=True
        )
        num_lines = len(raw_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum([line.text.rstrip().endswith(tuple(cls.dynamic_config.key_list)) for line in raw_lines])
        ratio = num_occurrences / num_lines
        if ratio > cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_INCOMPLETENESS'
            res.name = cls.__name__
            res.reason = "The ratio of lines end with ellipsis is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_INCOMPLETENESS", [])
class CommonLineEndWithTerminal(BaseRule):
    """check whether the ratio of line ends with terminal punctuation mark > 0.6 """
    dynamic_config = DynamicRuleConfig(threshold=0.6, key_list = [".", "!", "?", "”", "\""])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import TextSlice, split_paragraphs

        res = ModelRes()
        raw_content = input_data.content
        raw_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=lambda x: x, remove_empty=True
        )
        num_lines = len(raw_lines)
        if num_lines == 0:
            return res

        terminal_marks = [line.text.rstrip()[-1] for line in raw_lines if line.text and line.text.rstrip()[-1] not in cls.dynamic_config.key_list]
        num_occurrences = sum([line.text.rstrip().endswith(tuple(cls.dynamic_config.key_list)) for line in raw_lines])
        ratio = num_occurrences / num_lines
        if ratio < cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_INCOMPLETENESS'
            res.name = cls.__name__
            res.reason = list(set(terminal_marks))
        return res


@Model.rule_register("QUALITY_DISUNDERSTANDABILITY", ['sft','pretrain','benchmark'])
class CommonLineStartWithBulletpoint(BaseRule):
    """check whether the ratio of line starts with bullet points < 0.9 """
    dynamic_config = DynamicRuleConfig(
        threshold = 0.9,
        key_list = [
        "\u2022",  # bullet point
        "\u2023",  # triangular bullet point
        "\u25B6",  # black right pointing triangle
        "\u25C0",  # black left pointing triangle
        "\u25E6",  # white bullet point
        "\u25A0",  # black square
        "\u25A1",  # white square
        "\u25AA",  # black small square
        "\u25AB",  # white small square
        "\u2013",  # en dash
        ]
    )

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import TextSlice, split_paragraphs

        res = ModelRes()
        raw_content = input_data.content
        raw_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=lambda x: x, remove_empty=True
        )
        num_lines = len(raw_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum([line.text.lstrip().startswith(tuple(cls.dynamic_config.key_list)) for line in raw_lines])
        ratio = num_occurrences / num_lines
        if ratio > cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_DISUNDERSTANDABILITY'
            res.name = cls.__name__
            res.reason = "The ratio of lines start with bulletpoint is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_INEFFECTIVENESS", ['pretrain','benchmark'])
class CommonLineJavascriptCount(BaseRule):
    """check whether line with the word Javascript. """
    dynamic_config = DynamicRuleConfig(threshold=3)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import TextSlice, normalize, split_paragraphs

        res = ModelRes()
        raw_content = input_data.content
        normalized_lines: Tuple[TextSlice] = split_paragraphs(
            text=raw_content, normalizer=normalize, remove_empty=True
        )
        num_lines = len(normalized_lines)
        if num_lines == 0:
            return res

        num_occurrences = sum(['javascript' in line.text for line in normalized_lines])
        num_not_occur = num_lines - num_occurrences
        if num_not_occur < cls.dynamic_config.threshold and num_lines > 3:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = "The lines with the word Javascript is: " + str(num_occurrences)
        return res


@Model.rule_register("QUALITY_INEFFECTIVENESS", ['pretrain','benchmark'])
class CommonLoremIpsum(BaseRule):
    """check whether the ratio of lorem ipsum < 3e-08 """
    dynamic_config = DynamicRuleConfig(threshold=3e-08)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import normalize

        res = ModelRes()
        normalized_content = normalize(input_data.content)
        num_normalized_content = len(normalized_content)
        if num_normalized_content == 0:
            return res

        SEARCH_REGEX = re.compile(r"lorem ipsum", re.IGNORECASE)
        num_occurrences = len(SEARCH_REGEX.findall(normalized_content))
        ratio = num_occurrences / num_normalized_content
        if ratio > cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = "The ratio of lorem ipsum is: " + str(ratio)
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['pretrain'])
class CommonMeanWordLength(BaseRule):
    """check whether the mean length of word in [3, 10] """
    dynamic_config = DynamicRuleConfig(key_list=['3', '10'])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import normalize

        res = ModelRes()
        normalized_content = normalize(input_data.content)
        normalized_words = tuple(normalized_content.split())
        num_normalized_words = len(normalized_words)
        if num_normalized_words == 0:
            return res

        num_chars = float(sum(map(len, normalized_words)))
        mean_length = num_chars / num_normalized_words
        mean_length = round(mean_length, 2)
        if mean_length >= int(cls.dynamic_config.key_list[0]) and mean_length < int(cls.dynamic_config.key_list[1]):
            pass
        else:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = "The mean length of word is: " + str(mean_length)
        return res


@Model.rule_register('QUALITY_DISFLUENCY', ['default','sft','pretrain','benchmark','text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonNoPunc(BaseRule):
    """check whether paragraph has no punctuation."""
    dynamic_config = DynamicRuleConfig(threshold=112)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.detect_lang import decide_language_by_str

        res = ModelRes()
        content = input_data.content
        language = decide_language_by_str(content)
        if language != 'en':
            return res

        paragraphs = content.split('\n')
        longest_sentence = ''
        max_word_count = 0
        for paragraph in paragraphs:
            if len(paragraph.strip()) == 0:
                continue
            sentences = re.split("[–.!?,;•/|…]", paragraph)
            for sentence in sentences:
                words = sentence.split()
                word_count = len(words)
                if word_count > max_word_count:
                    max_word_count = word_count
                    longest_sentence = sentence.strip()
        if int(max_word_count) > cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_DISFLUENCY'
            res.name = cls.__name__
            res.reason = longest_sentence
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', [])
class CommonPatternSearch(BaseRule):
    """let user input pattern to search"""
    dynamic_config = DynamicRuleConfig(pattern = "your pattern")

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        matches = re.search(cls.dynamic_config.pattern, input_data.content)
        if matches:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = matches.group()
        return res


@Model.rule_register("QUALITY_INCOMPLETENESS", ['pretrain'])
class CommonSentenceNumber(BaseRule):
    """check whether the number of sentence in [3, 7500] """
    dynamic_config = DynamicRuleConfig(key_list=['3', '7500'])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        raw_content = input_data.content

        SENT_PATTERN = re.compile(r'\b[^.!?\n]+[.!?]*', flags=re.UNICODE)
        num_sentence = len(SENT_PATTERN.findall(raw_content))
        if num_sentence < int(cls.dynamic_config.key_list[0]) or num_sentence > int(cls.dynamic_config.key_list[1]):
            res.error_status = True
            res.type = 'QUALITY_INCOMPLETENESS'
            res.name = cls.__name__
            res.reason = "The number of sentence is: " + str(num_sentence)
        return res


@Model.rule_register('QUALITY_IRRELEVANCE', ['default','sft','pretrain','benchmark','text_base_all','llm_base','xyz_ar','xyz_ko','xyz_ru','xyz_th','xyz_vi','xyz_cs','xyz_hu','xyz_sr'])
class CommonSpecialCharacter(BaseRule):
    """check whether content has special characters. """
    dynamic_config = DynamicRuleConfig(
        key_list=[
            r"u200e",
            # r"(\\\\;){3,}|(\{\}){3,}|(&nbsp;){3,}",
            r"&#247;|\? :",
            r"[�□]|\{\/U\}",
            r"U\+26[0-F][0-D]|U\+273[3-4]|U\+1F[3-6][0-4][0-F]|U\+1F6[8-F][0-F]"
        ]
    )

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        content = input_data.content

        matches = []
        for p in cls.dynamic_config.key_list:
            m = re.findall(p, content)
            matches = matches + m
        if len(matches) != 0:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = list(set(matches))
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['pretrain'])
class CommonStopWord(BaseRule):
    """check whether the ratio of stop word > 0.06"""
    dynamic_config = DynamicRuleConfig(threshold=0.06)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from nltk.tokenize import WordPunctTokenizer

        from dingo.model.rule.common.detect_lang import decide_language_by_str
        from dingo.model.rule.common.util import get_stop_words

        res = ModelRes()
        raw_content = input_data.content
        language = decide_language_by_str(raw_content)
        if language != 'en':
            return res
        raw_words = list(WordPunctTokenizer().tokenize(raw_content))
        raw_words = [str(w).lower() for w in raw_words]
        num_raw_words = len(raw_words)
        if num_raw_words == 0:
            return res

        STOP_WORDS = get_stop_words("en")
        num_stop_words = sum(
            map(lambda w: w in STOP_WORDS, raw_words)
        )
        ratio = num_stop_words / num_raw_words
        if ratio < cls.dynamic_config.threshold or num_stop_words < 2:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = "The ratio of stop words is: " + str(ratio)
        return res


@Model.rule_register('QUALITY_INEFFECTIVENESS', ['pretrain','benchmark'])
class CommonSymbolWordRatio(BaseRule):
    """check whether the ratio of symbol and word is > 0.4"""
    dynamic_config = DynamicRuleConfig(threshold=0.4, key_list = ["#", "...", "…"])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from nltk.tokenize import WordPunctTokenizer

        res = ModelRes()
        raw_content = input_data.content
        raw_words = tuple(WordPunctTokenizer().tokenize(raw_content))
        num_raw_words = len(raw_words)
        if num_raw_words == 0:
            return res

        num_words = num_raw_words
        num_symbols = float(sum(
            raw_content.count(x) for x in cls.dynamic_config.key_list
        ))

        ratio = num_symbols / num_words
        if ratio > cls.dynamic_config.threshold:
            res.error_status = True
            res.type = 'QUALITY_INEFFECTIVENESS'
            res.name = cls.__name__
            res.reason = "The ratio of symbol / word is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_DISUNDERSTANDABILITY", ['pretrain'])
class CommonUniqueWords(BaseRule):
    """check whether the ratio of unique words > 0.1"""
    dynamic_config = DynamicRuleConfig(threshold=0.1)

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import normalize

        res = ModelRes()
        normalized_content = normalize(input_data.content)
        normalized_words = tuple(normalized_content.split())
        num_normalized_words = len(normalized_words)
        if num_normalized_words == 0:
            return res

        num_words = num_normalized_words
        num_unique_words = len(set(normalized_words))
        ratio = num_unique_words / num_words
        if ratio > cls.dynamic_config.threshold:
            pass
        else:
            res.error_status = True
            res.type = 'QUALITY_DISUNDERSTANDABILITY'
            res.name = cls.__name__
            res.reason = "The ratio of unique words is: " + str(ratio)
        return res


@Model.rule_register("QUALITY_IRRELEVANCE", [])
class CommonWatermark(BaseRule):
    """check whether content has watermarks."""
    dynamic_config = DynamicRuleConfig(key_list = [])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        res = ModelRes()
        matches = re.search('|'.join(cls.dynamic_config.key_list), input_data.content)
        if matches:
            res.error_status = True
            res.type = 'QUALITY_IRRELEVANCE'
            res.name = cls.__name__
            res.reason = matches.group()
        return res


@Model.rule_register("QUALITY_INCOMPLETENESS", ['pretrain'])
class CommonWordNumber(BaseRule):
    """check whether the number of word in [20, 100000] """
    dynamic_config = DynamicRuleConfig(key_list=['20', '100000'])

    @classmethod
    def eval(cls, input_data: MetaData) -> ModelRes:
        from dingo.model.rule.common.util import normalize

        res = ModelRes()
        normalized_content = normalize(input_data.content)
        normalized_words = tuple(normalized_content.split())
        num_normalized_words = len(normalized_words)
        if num_normalized_words >= int(cls.dynamic_config.key_list[0]) and num_normalized_words < int(cls.dynamic_config.key_list[1]):
            pass
        else:
            res.error_status = True
            res.type = 'QUALITY_INCOMPLETENESS'
            res.name = cls.__name__
            res.reason = "The number of word is: " + str(num_normalized_words)
        return res


if __name__ == '__main__':
    data = MetaData(
        data_id = '',
        prompt = '',
        content = "FA OR FICTION? WH CA IT DO?{{{{{{{{{{{"
    )
    tmp = CommonSentenceNumber().eval(data)
    print(tmp)