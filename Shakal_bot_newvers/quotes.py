import random

# Списки для подстановки
patsany = ["пацаны", "волки", "матери", "девки", "отцы", "братья"]
komu = ["матерям", "пацанам", "волкам", "девкам", "отцам", "братьям"]
volk = ["волк", "тот", "кто", "брат"]
wolf = ["Волк", "Лев", "Тигр", "Пацан", "Мать", "Клоун"]
lion = ["льва", "тигра", "волка", "пацана", "матери", "клоуна"]
circus = ["в цирке", "на сцене", "на манеже"]
act = ["выступает", "бухает", "поёт", "танцует"]

# Шаблоны для генерации
templates = [
    "Не гоняйте, {patsany}, вы {komu} ещё нужны",
    "Не {тот|кто} [volk], {тот|кто} [volk], а {тот|кто|тот, что} [volk]",
    "[wolf] {слабее|сильнее} [lion] и [lion], но [circus]{ не|} [act]",
    "Каждый {думает|знает}, что {думает|знает} меня, но не каждый {думает|знает}, что {думает|знает}",
    "{Неважно|Важно}, кто {кто|напротив|рядом}, {неважно|важно}, кто {кто|напротив|рядом}",
    "//Лучше иметь {врага|друга|друг друга|подругу}, чем {врага|друга|друг друга|подругу}",
    "{[volk.titleCase]|[wolf]}{ не|} {[act]|[volk]}{ [lion]| [komu]|}, {но|а|кто}{ не|} {[act]|[volk]}, {тот|кто}{ не|} {[volk]|[wolf.lowerCase]}"
]

# Функция для замены шаблонов на случайные значения
def generate_quote():
    # Выбираем случайный шаблон
    template = random.choice(templates)

    # Заменяем плейсхолдеры на случайные значения
    while '{' in template:
        start = template.find('{')
        end = template.find('}', start)
        placeholder = template[start+1:end]

        # Разделяем по '|' для выбора случайного варианта
        options = placeholder.split('|')
        replacement = random.choice(options)

        # Заменяем placeholder на выбранное значение
        template = template[:start] + replacement + template[end+1:]

    while '[' in template:
        start = template.find('[')
        end = template.find(']', start)
        placeholder = template[start+1:end]

        # Выбираем случайное значение для подстановки
        if placeholder == "patsany":
            replacement = random.choice(patsany)
        elif placeholder == "komu":
            replacement = random.choice(komu)
        elif placeholder == "volk":
            replacement = random.choice(volk)
        elif placeholder == "wolf":
            replacement = random.choice(wolf)
        elif placeholder == "lion":
            replacement = random.choice(lion)
        elif placeholder == "circus":
            replacement = random.choice(circus)
        elif placeholder == "act":
            replacement = random.choice(act)
        else:
            replacement = placeholder

        # Заменяем placeholder на выбранное значение
        template = template[:start] + replacement + template[end+1:]

    return template

# Пример генерации цитаты
#print(generate_quote())
