link_source_code = "https://"
tg_nickname =  "@rombintu"
commands = [
    "/help - Помощь", 
    "/expenses - Отчет за текущий месяц", 
    "/month - Отчет за прошлый месяц", 
    ]
start_message = f"Привет, я помогу тебе вести учет твоих финансов"\
                f"\n\nИсходный код: {link_source_code}" \
                f"\n\nФидбек и баги: {tg_nickname}" \
                "\n\n{}".format('\n'.join(commands))

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