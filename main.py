# local imports
# import os, sys

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
def handle_message_week(message):
    uuid = message.chat.id
    response = content.report.format("текущий месяц")
    notes, err = db.get_notes(uuid, scope="current_month")
    if err: 
        response = content.error_some.format(content.operations["r"])
        print(err)
    else:
        response += utils.fnotes(notes)
    finbot.send_message(message.chat.id, response)

@finbot.message_handler(commands=['month'])
def handle_message_week(message):
    uuid = message.chat.id
    response = content.report.format("прошлый месяц")
    notes, err = db.get_notes(uuid, scope="last_month")
    if err: 
        response = content.error_some.format(content.operations["r"])
        print(err)
    else:
        response += utils.fnotes(notes)
    finbot.send_message(message.chat.id, response)

@finbot.message_handler(content_types=["text"])
def handle_message_text(message):
    uuid = message.chat.id
    response = content.success.format(content.operations["w"])
    note = validator.filter_by_input(message.text)
    
    if note["cost"] < 0:
        finbot.send_message(uuid, content.error_input)
        return
    else:
        exist, err = db.category_is_exist(uuid, note["category"])
        if err: 
            finbot.send_message(uuid, content.error_some.format(content.operations["w"]))        
            print(err)
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
        ok, err = db.create_one(database.Note(
            uuid=uuid,
            cost=note["cost"],
            category=note["category"],
            comment=note["comment"],
            )
        )
        if err or not ok: 
            response = content.error_some.format(content.operations["w"])
            print(err)
    finbot.send_message(uuid, response)

def new_category(message, note):
    uuid = message.chat.id
    response = content.success.format(content.operations["w"])
    if message.text == "Добавить":
        ok, err = db.create_one(database.Note(
            uuid=uuid,
            cost=note["cost"],
            category=note["category"],
            comment=note["comment"],
            )
        )
        if err or not ok: 
            response = content.operations.format(content.operations["w"])
            print(err)
    else:
        response = content.operations["cancel"]
    finbot.send_message(uuid, response)

def main():
    print("Service status: OK")
    finbot.polling(none_stop=True, timeout=60)

if __name__ == "__main__":
    main()