link_source_code = "https://github.com/rombintu/pyfinbot.git"
tg_nickname =  "@rombintu"
commands = [
    "/help - Помощь", 
    "/expenses - Отчет за текущий месяц", 
    "/month - Отчет за прошлый месяц",
    "/settings - Настройка сервиса",
    ]

futures = [
    "/cancel - Отмена последней операции",
    "/analytics - Смарт аналитика",
    "rub|usd - Настройка отчета в разных курсах",
]
start_message = f"Привет, я помогу тебе вести учет твоих финансов"\
                f"\n\nФидбек и баги: {tg_nickname}" \
                "\n\n{}".format('\n'.join(commands)) +\
                "\n\nВ следующих версиях ожидаются функции:{}".format('\n'.join(futures)) +\
                f"\n\nИсходный код: {link_source_code}" \

error_input = "Неправильный ввод.\nОжидается: Стоимость Категория"
error_some = "Операция {} не прошла. Обратитесь к администратору"
success = "Операция {} прошла успешно"

new_category = "Категория [{}] не найдена в базе данных, хотите добавить?"
report = "Отчет за {}:\n"
operations = {
    "w": "записи", 
    "r": "чтения",
    "cancel": "Отмена операции"
}
headers_for_table = ["Категория", "Сумма"]