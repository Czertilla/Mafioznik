language_codes = ('ru', 'en')
languages = {
    'ru': 'Русский',
    'en': 'English'
}

with open(".git/COMMIT_EDITMSG") as f:
    version = f.readline()

def welcome_back (name):
    return {
        'ru': f"С возвращением, {name}!",
        'en': f"Welcome back, {name}!"
    }

def welcome (name):
    return {
        'ru': f"Добро пожаловать, {name}",
        'en': f"Welcome {name}"
    }

def helping (nav):
    if nav == 'mm':
        return {
            'ru': f"Вы находитесь в главном меню телеграм-бота Mafioznik — ассистента-помощника для игры в Мафию \nВНИМАНИЕ, ПРОДУКТ НАХОДИТСЯ В АЛЬФА-РАЗРАБОТКЕ:\n{version}/connect - Присоедениться к игре\n/create - Создать лобби\n/profile - Зайти в меню профиля\n/about - Узнать про игру Мафия",
            'en': f"You are in the main menu of the Mafioznik telegram bot, an assistant for playing Mafia \nATTENTION, THE PRODUCT IS IN ALPHA DEVELOPMENT:\n{version}/connect - Connect to the game\n/create - Create a lobby\n/profile - Go to the profile menu\n/about - Learn about Mafia"
        }
    if nav == 'pm':
        return {
            'ru': f"Вы находитесь в меню профиля игрока в Мафию. Вы были автоматически зарегистрированы при нажатии на кнопку <<Старт>>. Здесь вы можете управлять вашим профилем или смотреть интересующую вас информацию\n/update - Обновить информацию о профиле\n/stats - Посмотреть статистику\n/language - Изменить язык\n/discard - Удалить ваш игровой профиль (без возможности восстановления, с сервера удалится вся информация о вас, сбросится вся статистика). Если вы захотите снова начать с чистого листа, просто снова авторизируйтесь",
            'en': f"You are in the player profile menu in Mafia. You have been automatically registered by clicking <<Start>>. Here you can manage your profile or view the information you are interested in\n/update - Update profile information\n/stats - View statistics\n/language - Change language\n/discard - Delete your gaming profile (no option to recovery, all information about you is deleted from the server, all statistics are reset). If you use again from scratch, just log in again"
        }
    if nav == 'lo':
        return {
            'ru': f"Вы находитесь в лобби и скоро начнете играть в Мафию. \n/info - Просмотреть информацию о лобби\n/chat - Получить ссылку чата\n/quit - Выйти из лобби",
            'en': f"You are in the lobby and will start playing Mafia soon. \n/info - View information about the lobby\n/chat - Get a chat link\n/quit - Quit the lobby"
        }
    
def main_menu(but=''):
    buts = {
        '': {
            'ru': 'Главное меню',
            'en': 'Main menu'
        },
        'connect': {
            'ru': 'Присоедениться к лобби',
            'en': 'Join lobby'
        },
        'create': {
            'ru': 'Создать лобби',
            'en': 'Create a lobby'
        },
        'profile': {
            'ru': 'Меню профиля',
            'en': 'Profile menu'
        }
    }
    return buts[but]

def profile_menu(but=''):
    buts = {
        '': {
            'ru': "\tМеню профиля",
            'en': "\tProfile menu"
        },
        'update':
        {
            'ru': "Обновить данные профиля",
            'en': "Update profile information"
        },
        "stats":
        {
            'ru': "Статистика",
            'en': "Statistics"
        },
        "language":
        {
            'ru': "Язык",
            'en': "Language"
        },
        "discard":
        {
            'ru': "Удалить профиль",
            'en': "Discard profile"
        }
    }
    return buts[but]

def commit(case):
    cases = {
        'cl': {
            'ru': 'Язык сменен',
            'en': 'Language changed'
        },
        'pu': {
            'ru': 'Профиль обновлен',
            'en': 'Profile updated'
        }
    }
    return cases[case]

def stats(user):
    return {
        'ru': f"На данный момент здесь отображается информация о профиле\nИмя: {user['first_name']}\nФамилия: {user['last_name']}\nНикнейм: {user['username']}\nРепутация: {user['reputation']}\nСтатус: {user['status']}\nДата регистрации: {user['registered']}",
        'en': f"Profile information is currently displayed here\nName: {user['first_name']}\nLast name: {user['last_name']}\nNickname: {user['username']}\nReputation: {user['reputation']}\nStatus: {user['status']}\nRegistration Date: {user['registered']}"
    }

def lang_list ():
    return {
        'ru': f"Вот доступные языки",
        'en': f"Here are the available languages"
    }

def confirm (name):
    return {
        'ru': f"Вы собираетесь удалить свой игровой профиль в системе Mafioznik. Вся информация о вас будет удалена из базы данных бота: Информация профиля, статистика в игре и тд. У вас не будет возможности восстановить эту информацию, только создать полностью новый профиль.\n Для подтверждения этого действия напишите: {name}\nДля отмены действия напишите что угодно отличное",
        'en': f"You are about to delete your gaming profile in the Mafioznik system. All information about you will be deleted from the bot database: profile information, game statistics, etc. You will not be able to restore this information, only create a completely new profile.\n To confirm this action, write:\n{name}\nTo cancel an action, write something different"
    }

def after_discard ():
    return {
        'ru': f"Ваш профиль был удален. Чтобы создать новый, пропишите команду \n/start",
        'en': f"Your profile has been deleted. To create a new one, write the command \n/start"
    }