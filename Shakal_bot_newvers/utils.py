import re
import random
from pymystem3 import Mystem

mystem = Mystem()

TRIGGERS = [
    (re.compile(r'^к[оа]роч[ье]?$', re.I), 'У кого короче, тот дома сидит!'),
    (re.compile(r'^нет$', re.I), 'Пидора ответ!'),
    (re.compile(r'^хо(чу|тим|тят|тел|тела)$', re.I), 'Хотеть невредно!'),
]

ANSWER_TO_QUESTION = "А тебя ебёт?"
QUESTION_WORDS = ["когда", "где", "почему", "зачем", "как", "сколько", "что", "кто"]

VOWEL_TO_RHYME = {"а": "я", "о": "ё", "у": "ю", "е": "е", "ы": "и", "и": "и", "э": "е", "ю": "ю", "я": "я"}
VOWELS = "аоуыэеёиюя"


def get_words(text):
    """ Разбивает текст на слова """
    return re.findall(r'\b\w+\b', text.lower())


def get_by_word_trigger(text):
    """ Проверяет текст на соответствие триггерам """
    for word in get_words(text):
        for pattern, response in TRIGGERS:
            if pattern.match(word):
                return response
    return None


def get_answer_to_question(text):
    """ Проверяет, является ли текст вопросом """
    if text.strip().endswith("?") or any(qw in text.lower() for qw in QUESTION_WORDS):
        return ANSWER_TO_QUESTION
    return None


def get_first_syllable(word):
    """ Возвращает первый слог в слове """
    syllable = ""
    for letter in word:
        syllable += letter
        if letter in VOWELS:
            break
    return syllable


def get_rhyme(word):
    """ Генерирует рифму для слова """
    # Используем Mystem для морфологического анализа
    parsed = mystem.analyze(word)
    if not parsed or "analysis" not in parsed[0] or not parsed[0]["analysis"]:
        return None

    # Проверка, является ли слово существительным или прилагательным
    lexeme = parsed[0]["analysis"][0]["lex"]
    tag = parsed[0]["analysis"][0].get("gr", "")
    if "S" not in tag and "A" not in tag:  # "S" - существительное, "A" - прилагательное
        return None

    syllable = get_first_syllable(word)
    if not syllable or syllable == word:
        return None

    new_vowel = VOWEL_TO_RHYME.get(syllable[-1], syllable[-1])
    return f"ху{new_vowel}{word[len(syllable):]}"


def get_rhymes(text):
    """ Возвращает список рифм для текста """
    return [get_rhyme(word) for word in get_words(text) if get_rhyme(word)]
