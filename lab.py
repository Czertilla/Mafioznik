import telebot
import sqlite3

con = sqlite3.connect("db/users.db", check_same_thread=False)
cur = con.cursor()


def db_table_val(id: int, first_name: str, last_name: str, username: str):
    cur.execute('INSERT INTO test (id, username, first_name, last_name) \
        VALUES (?, ?, ?, ?)', (id, username, first_name, last_name))
    con.commit()

bot = telebot.TeleBot("5392200451:AAETSpaOC3XepS3cqvOGz0RHjSO7I1ImKlE")

@bot.message_handler(commands=["start"])
def start(message):
    user = message.from_user
    id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    db_table_val(id, first_name, last_name, username)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.from_user.id, "Для авторизации в системе пропишите команду\
         /verify")


@bot.message_handler(commands=["verify"])
def verify(message):
    user = message.from_user
    id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    db_table_val(id, first_name, last_name, username)



bot.polling(none_stop=True, interval=0)