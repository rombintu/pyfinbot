# local imports
# import os, sys
import logging
# external imports
import telebot
from telebot import types

# internal imports
from internal import content, database
from tools import validator, parser, utils

envs = parser.parse_dotenv()

finbot = telebot.TeleBot(envs["TOKEN"], parse_mode=None)
db = database.Database(envs["DATABASE"], dev=True)

@finbot.message_handler(commands=['start', 'help'])
def handle_message_start(message):
    finbot.send_message(
        message.chat.id, 
        content.start_message
    )

@finbot.message_handler(commands=['expenses'])
def handle_message_expenses(message):
    uuid = message.chat.id
    response = content.report.format("текущий месяц")
    notes, err = db.get_notes(uuid, scope="current_month")
    if err: 
        response = content.error_some.format(content.operations["r"])
        logging.error(err)
    else:
        response += utils.fnotes(notes)
    finbot.send_message(message.chat.id, response)

@finbot.message_handler(commands=['month'])
def handle_message_month(message):
    uuid = message.chat.id
    response = content.report.format("прошлый месяц")
    notes, err = db.get_notes(uuid, scope="last_month")
    if err: 
        response = content.error_some.format(content.operations["r"])
        logging.error(err)
    else:
        response += utils.fnotes(notes)
    finbot.send_message(message.chat.id, response)

@finbot.message_handler(commands=['settings'])
def handle_message_settings(message):
    uuid = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    limit_keyboard = types.InlineKeyboardButton(text="Ограничитель", callback_data="limit")
    keyboard.add(limit_keyboard)
    finbot.send_message(uuid, "Настройки ⚙️", reply_markup=keyboard)

@finbot.callback_query_handler(func=lambda call: True)
def callback_funcs(call):
    uuid = call.message.chat.id
    if call.data == "limit":
        categories, err = db.get_categories(uuid)
        limits, err = db.get_limit_all(uuid)
        response = content.limit_info
        if not limits:
            response = content.some_is_empty.format("Ограничения")
        else:
            response += "\n".join([f"{cat.title()} - {utils.fcost(summ)}" for cat, summ in limits])

        finbot.send_message(uuid, response)

        if err:
            finbot.send_message(uuid, content.error_some.format(content.operations["w"]))
            logging.error(err)
            return
        elif not categories:
            finbot.send_message(uuid, content.some_is_empty.format("Категории"))
            return
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for category in categories:
            keyboard.row(str(category).title())

        finbot.send_message(uuid, 
            content.update_limit_category, reply_markup=keyboard)
        finbot.register_next_step_handler(call.message, update_limit)
    elif call.data == "unlimit":
        category = call.message.text.split()[-1].lower()
        err = db.update_limit_by_category(uuid, category, 0)
        if err:
            finbot.send_message(uuid, content.error_some.format(content.operations["w"]))
            logging.error(err)
            return
        # Delete message
        finbot.delete_message(uuid, call.message.message_id)
    elif call.data == "undo":
        args = call.message.text.split()
        category = args[-1]
        cost = int(args[-2])
        note = database.Note(cost=-cost, category=category, comment="delete")
        ok, err = db.create_note(uuid, note)
        if err or not ok: 
            response = content.error_some.format(content.operations["w"])
            logging.error(err)
            return
        # Delete message
        finbot.delete_message(uuid, call.message.message_id)
    else:
        finbot.send_message(uuid, "PASS")

def update_limit(message):
    """
    Request limit cost
    """
    uuid = message.chat.id
    if message.text == "/cancel":
        finbot.send_message(uuid, content.cancel, reply_markup=None)
        return
    select_category = (message.text).lower()
    finbot.send_message(uuid, content.update_limit_cost)
    finbot.register_next_step_handler(message, update_limit_cost, select_category)

def update_limit_cost(message, category):
    uuid = message.chat.id
    if message.text == "/cancel":
        finbot.send_message(uuid, content.cancel, reply_markup=None)
        return
    response = content.success_w
    limit = validator.find_K_in_int(message.text)
    err = db.update_limit_by_category(uuid, category, limit)
    if err or limit < 0:
        response = content.error_some.format(content.operations["w"])
        logging.error(err)
    finbot.send_message(uuid, response.format(limit, category))

@finbot.message_handler(content_types=["text"])
def handle_message_text(message):
    uuid = message.chat.id
    response = content.success_w
    note = validator.filter_by_input(message.text)

    if note["cost"] < 0:
        finbot.send_message(uuid, content.error_input)
        return
    else:
        exist, err = db.category_is_exist(uuid, note["category"])
        if err: 
            finbot.send_message(uuid, content.error_some.format(content.operations["w"]))        
            logging.error(err)
            return
        elif not exist:
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard.row("Отмена", "Добавить")
            finbot.send_message(uuid, content.new_category.\
                format(note["category"].title()),
                reply_markup=keyboard
            )
            finbot.register_next_step_handler(message, new_category, note)
            return
        trigger, err = db.trigger_by_limit(uuid, category=note["category"])
        if trigger:
            callback_keyboard_trigger = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text="Убрать ограничение", callback_data="unlimit")
            callback_keyboard_trigger.add(btn)
            finbot.send_message(uuid, content.trigger_limit.format(note["category"].title()), reply_markup=callback_keyboard_trigger)

        dbnote = database.Note(
            cost=note["cost"],
            category=note["category"],
            comment=note["comment"],
        )
        ok, err = db.create_note(uuid, dbnote)
        if err or not ok: 
            response = content.error_some.format(content.operations["w"])
            logging.error(err)
    callback_keyboard = types.InlineKeyboardMarkup()
    btn_scs = types.InlineKeyboardButton(text="Отмена операции", callback_data="undo")
    callback_keyboard.add(btn_scs)
    finbot.send_message(uuid, response.format(note["cost"], note["category"]), reply_markup=callback_keyboard)

def new_category(message, note):
    uuid = message.chat.id
    response = content.success_w
    callback_keyboard = types.InlineKeyboardMarkup()
    btn_scs = types.InlineKeyboardButton(text="Отмена операции", callback_data="undo")
    callback_keyboard.add(btn_scs)
    if message.text == "Добавить":
        dbnote = database.Note(
            cost=note["cost"],
            category=note["category"],
            comment=note["comment"],
        )
        ok, err = db.create_note(uuid, dbnote)
        if err or not ok: 
            response = content.error_some.format(content.operations["w"])
            logging.error(err)
    else:
        response = content.operations["cancel"]
        callback_keyboard = types.InlineKeyboardMarkup()
    finbot.send_message(uuid, response.format(note["cost"], note["category"]), reply_markup=callback_keyboard)

def main():
    logging.debug("Service status: OK")
    finbot.polling(none_stop=True, timeout=60)

if __name__ == "__main__":
    main()