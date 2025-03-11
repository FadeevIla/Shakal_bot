import random
from pymystem3 import Mystem

# Инициализируем Mystem
mystem = Mystem()

# Списки для подстановки с падежами
placeholders = {
    "patsany": ["пацаны", "волки", "матери", "девки", "отцы", "братья"],
    "komu": ["матерям", "пацанам", "волкам", "девкам", "отцам", "братьям"],
    "volk": ["волк", "тот", "брат"],
    "wolf": ["Волк", "Лев", "Тигр", "Пацан", "Клоун"],  # Убрал "Мать", т.к. здесь муж. род
    "lion": ["льва", "тигра", "волка", "пацана", "клоуна"],  # Убрал "матери", т.к. дательный
    "circus": ["в цирке", "на сцене", "на манеже"],
    "act": ["выступает", "бухает", "поёт", "танцует"],
    "money": ["деньги", "баксы", "пачки", "зелёные"],
    "fear": ["страх", "панику", "ужас", "жесть"],
    "life": ["жизнь", "судьбу", "путь", "реальность"],
    "success": ["успех", "достижение", "победу", "фарт"],
    "power": ["силу", "мощь", "власть"],
    "heart": ["сердце", "душу", "мозги", "эмоции"],
    "nature": ["природа", "окружающий мир", "вселенная"],
    "respect": ["уважение", "почёт", "авторитет", "респект"],
    "law": ["закон", "понятия", "кодекс", "правила"],
    "road_nom": ["путь", "дорога", "маршрут", "тропа"],
    "road_acc": ["путь", "дорогу", "маршрут", "тропу"],
    "enemy_nom": ["враг", "предатель", "крыса", "недруг"],
    "enemy_gen": ["врага", "предателя", "крысы", "недруга"],
    "friend_nom": ["брат", "кореш", "товарищ", "друг"],
    "friend_gen": ["брата", "кореша", "товарища", "друга"],
    "time": ["время", "моменты", "жизнь", "часы"],
    "pain": ["боль", "страдания", "испытания", "потери"],
    "lesson": ["урок", "опыт", "испытание", "жизненную мудрость"]
}

# Шаблоны для генерации
templates = [
    "Не гоняйте, {patsany}, вы {komu} ещё нужны.",
    "[volk] {слабее|сильнее} [lion], но [circus] {не|} [act].",
    "{money} не принесут тебе {success}, если {life} не будет твоим другом.",
    "Тот, кто не боится {fear}, {act} с {power}.",
    "{nature} учит нас, что каждый {volk} — это {heart}.",
    "Жизнь — это {nature}, и в её {life} каждый найдёт свой путь.",
    "Кто не уважает {respect}, тот не знает {law}.",
    "Лучше идти своим {road_acc}, чем следовать за {enemy_nom}.",
    "{time} покажет, кто {friend_nom}, а кто {enemy_nom}.",
    "В {pain} рождается {lesson}, а в {lesson} — {power}.",
    "Не предаст {friend_nom}, кто знает цену {respect}.",
    "На {road_nom} встречаются {friend_nom} и {enemy_nom}, важно не спутать {friend_gen} с {enemy_gen}.",
    "Если {time} даёт тебе {lesson}, прими его, как {friend_nom}.",
    "{respect} нельзя купить за {money}, его можно только заслужить.",
    "Кто идёт своим {road_nom}, тот сам пишет свой {law}.",
    "В {pain} находишь правду, а в правде — свою силу."
]

def apply_case(word, case):
    """Применяет падеж к слову с помощью Mystem."""
    analyzed = mystem.analyze(word)
    if analyzed and 'analysis' in analyzed[0] and analyzed[0]['analysis']:
        lex = analyzed[0]['analysis'][0].get('lex', word)
    else:
        lex = word  # Если анализ не удался, используем оригинальное слово

    if case == "gen":
        # Родительный падеж
        return mystem.lemmatize(lex)[0] + "а"
    elif case == "acc":
        # Винительный падеж
        return mystem.lemmatize(lex)[0]
    elif case == "dat":
        # Дательный падеж
        return mystem.lemmatize(lex)[0] + "у"
    else:
        # Именительный падеж (по умолчанию)
        return mystem.lemmatize(lex)[0]

def generate_quote():
    """Генерирует случайную цитату с учетом падежей."""
    template = random.choice(templates)

    while '{' in template:
        start = template.find('{')
        end = template.find('}', start)
        placeholder = template[start + 1:end]

        if placeholder in placeholders:
            replacement = random.choice(placeholders[placeholder])
        else:
            options = placeholder.split('|')
            replacement = random.choice(options)

        # Определяем падеж из плейсхолдера
        if "gen" in placeholder:
            replacement = apply_case(replacement, "gen")
        elif "acc" in placeholder:
            replacement = apply_case(replacement, "acc")
        elif "dat" in placeholder:
            replacement = apply_case(replacement, "dat")
        else:
            replacement = apply_case(replacement, "nom")

        template = template[:start] + replacement + template[end + 1:]

    return template

# Пример использования
if __name__ == "__main__":
    print(generate_quote())