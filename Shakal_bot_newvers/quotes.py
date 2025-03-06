import random
from pymystem3 import Mystem

# Инициализируем Mystem
mystem = Mystem()

# Списки для подстановки с падежами
placeholders = {
    "patsany": ["пацаны", "волки", "матери", "девки", "отцы", "братья"],
    "komu": ["матерям", "пацанам", "волкам", "девкам", "отцам", "братьям"],
    "volk": ["волк", "тот", "кто", "брат"],
    "wolf": ["Волк", "Лев", "Тигр", "Пацан", "Мать", "Клоун"],
    "lion": ["льва", "тигра", "волка", "пацана", "матери", "клоуна"],
    "circus": ["в цирке", "на сцене", "на манеже"],
    "act": ["выступает", "бухает", "поёт", "танцует"],
    "money": ["деньги", "баксы", "пачки", "зелёные"],
    "fear": ["страх", "панику", "ужас", "жесть"],
    "life": ["жизнь", "судьбу", "путь", "реальность"],
    "success": ["успех", "достижение", "победу", "фарт"],
    "power": ["силу", "мощь", "власть"],
    "heart": ["сердце", "душу", "мозги", "эмоции"],
    "nature": ["природа", "окружающий мир", "земля", "вселенная"],
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

# Функция для генерации цитаты
def generate_quote():
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

        # Применяем падежи через Mystem
        analyzed = mystem.analyze(replacement)

        # Получаем лемму и обрабатываем падежи в зависимости от типа
        lex = analyzed[0].get('lex', replacement)

        if "gen" in placeholder:
            # Генерация родительного падежа
            replacement = mystem.lemmatize(lex)[0]
            replacement = replacement + "а" if replacement.endswith("й") else replacement
        elif "acc" in placeholder:
            # Генерация винительного падежа
            replacement = mystem.lemmatize(lex)[0]
        elif "dat" in placeholder:
            # Генерация дательного падежа
            replacement = mystem.lemmatize(lex)[0] + "у" if lex.endswith("ь") else replacement
        else:
            replacement = mystem.lemmatize(lex)[0]  # Лемматизация без изменения падежа

        template = template[:start] + replacement + template[end + 1:]

    return template

# Пример использования
print(generate_quote())
