import telebot
# import sqlite3
import base
# con = sqlite3.connect("db/users.db", check_same_thread=False)
# cur = con.cursor()


# def db_table_val(id: int, first_name: str, last_name: str, username: str):
#     cur.execute('INSERT INTO test (id, username, first_name, last_name) \
#         VALUES (?, ?, ?, ?)', (id, username, first_name, last_name))
#     con.commit()


users_data = base.Base('u')
bot = telebot.TeleBot("5392200451:AAETSpaOC3XepS3cqvOGz0RHjSO7I1ImKlE")


@bot.message_handler(commands=["update"])
def update(message):
    user = message.from_user
    d = vars(user)
    dic = {}
    print(locals())
    for i in d:
        dic[i] = locals().get("user."+i)
    users_data.update_profile(user.id, {'user': user})



bot.polling(none_stop=True, interval=0)
