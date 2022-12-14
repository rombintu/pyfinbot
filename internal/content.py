link_source_code = "https://github.com/rombintu/pyfinbot.git"
tg_nickname =  "@rombintu"
commands = [
    "/help - Помощь", 
    "/expenses - Отчет за текущий месяц", 
    "/month - Отчет за прошлый месяц",
    "/settings - Настройка сервиса",
    ]

futures = [
    "Команда: /analytics - Умная аналитика",
    "Функционал: rub|usd - Настройка отчета в разных валютах СНГ",
]
start_message = f"Привет, я помогу тебе вести учет твоих финансов"\
                f"\n\nФидбек и баги: {tg_nickname}" \
                "\n\n{}".format('\n'.join(commands)) +\
                "\n\nВ следующих версиях ожидаются функции:{}".format('\n'.join(futures)) +\
                f"\n\nИсходный код: {link_source_code}" \

error_input = """Неправильный ввод.\nОжидается: Стоимость[к[$]] Категория
Примеры:
200 обед - Добавить 200р в [Обед]
10к отпуск - Добавить 10,000р в [Отпуск]
15к$ инвестиции - Добавить 15,000*$ в [Инвестиции]"""

error_some = "Операция {} не прошла. Обратитесь к администратору"
error_limit = "Лимит должен быть положительным числом"
success_w = "Операция записи прошла успешно: {} {}"
success_r = "Операция чтения прошла успешно"
cancel = "Отмена текущей операции..."
new_category = "Категория [{}] не найдена в базе данных, хотите добавить?"
report = "Отчет за {}:\n"
operations = {
    "w": "записи", 
    "r": "чтения",
    "cancel": "Отмена операции"
}
headers_for_table = ["Категория", "Сумма"]

update_limit_category = "Выбери категорию на которую хочешь поставить лимит [/cancel]"
update_limit_cost = "Укажи сумму которую не хочешь превышать в месяц [/cancel]"
some_is_empty = "[{}] В базе данных ничего не найдено"
limit_info = """Я буду оповещать тебя, если лимит будет превышен

Если хочешь убрать ограничение, укажи категории сумму 0

Ограничение действует на:\n"""

trigger_limit = "⚠️ Обращаю внимание, что месячный лимит превышен на категорию: {}"