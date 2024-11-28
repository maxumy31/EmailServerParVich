import sqlite3
import asyncio
connection = sqlite3.connect("data2.db")
email_domain = "test.ru"

async def registerDB():
    cursor = connection.cursor()
    await asyncio.to_thread(cursor.execute('''
    CREATE TABLE IF NOT EXISTS Mail(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme TEXT,
    content TEXT,
    author INTEGER,
    sentTo INTEGER
    )
    '''))#Таблица с почтой


    await asyncio.to_thread(cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE
    )
    '''))#Таблица с пользователями
    connection.commit()

async def create_email(email):
    if "@" not in email:
        error = f"{email} не соответсвует правилам формата"
        print(error)
        return (False,error)

    input_domain = email.split("@")[1]
    if(input_domain != email_domain):
        error = f"{email} не соответсвует название домена"
        print(error)
        return (False,error)

    try:
        cursor = connection.cursor()
        await asyncio.to_thread(cursor.execute('''
            INSERT INTO Users (email) 
            VALUES (?)
        ''', (email,)))
        connection.commit()
        success = f"Пользователь {email} был успешно создан"
        print(success)
        return (True,success)
    except sqlite3.Error as e:
        error = f"Ошибка при создании пользователя: {e}"
        print(error)
        return (False,error)

    connection.commit()
async def check_email_exists(email):
    cursor = connection.cursor()
    await asyncio.to_thread(cursor.execute('''
    SELECT * FROM Users WHERE email = ?
    ''', (email,)))
    user = cursor.fetchone()

    if user:
        result = f"Почта {email} существует."
        print(result)
        return(True,user)
    else:
        result = f"Почты {email} не существует"
        print(result)
        return(False,None)

def send_mail(theme,content,author_id,sent_to_id):
    try:
        cursor = connection.cursor()
        await asyncio.to_thread(cursor.execute('''
            INSERT INTO Mail (theme,content,author,sentTo) 
            VALUES (?,?,?,?)
        ''', (theme,content,author_id,sent_to_id)))
        connection.commit()
        success = f"Письмо от {author_id} до {sent_to_id} было успешно добавлено"
        print(success)
        return (True,success)
    except sqlite3.Error as e:
        error = f"Ошибка при добавлении письма {e}"
        print(error)
        return (False,error)

def get_mail_for_email(email):
    user = check_email_exists(email)
    if(user[1] == None):
        return(False,"Пользователь не найден")
    print(user)
    userID = user[1][0]
    print("ID = ",userID)
    cursor = connection.cursor()
    await asyncio.to_thread(cursor.execute('''
        SELECT * FROM Mail WHERE author = ?
    ''', (userID,)))
    data = cursor.fetchall()
    return(True,data)

def close():
    connection.close()