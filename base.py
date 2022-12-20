import sqlite3

class Base:
    def __init__(self):
        self.users = {}
        try:
            sqlite_connection = sqlite3.connect('bases/users.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sqlite_select_query = """SELECT * from sqlitedb_developers"""
            cursor.execute(sqlite_select_query)
            print("Чтение")
            records = cursor.fetchall()
            for row in records:
                ID = row[0]
                self.users[ID] = {
                    "ID": ID,
                    "username": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "language_code": row[4],
                    "session": row[5],
                    "kills": row[6],
                    "deaths": row[7],
                    "complicities": row[8],
                    "rescues": row[9],
                    "wins": row[10],
                    "defeats": row[11],
                    "exiles": row[12],
                    "reputation": row[13],
                    "banned": row[14],
                    "registered": row[15],
                    "status": row[16],
                    "rights_lvl": row[17]
                }

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

        self.games = {}
        try:
            sqlite_connection = sqlite3.connect('bases/games.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sqlite_select_query = """SELECT * from sqlitedb_developers"""
            cursor.execute(sqlite_select_query)
            print("Чтение")
            records = cursor.fetchall()
            for row in records:
                ID = row[0]
                self.games[ID] = {
                    "ID": ID,
                    "status": row[1],
                    "users": row[2],
                    "last_name": row[3],
                    "language_code": row[4],
                    "session": row[5],
                    "kills": row[6],
                    "deaths": row[7],
                    "complicities": row[8],
                    "rescues": row[9],
                    "wins": row[10],
                    "defeats": row[11],
                    "exiles": row[12],
                    "reputation": row[13],
                    "banned": row[14],
                    "registered": row[15],
                }

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")