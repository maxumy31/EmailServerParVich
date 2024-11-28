import sqlite3
import threading

DB_PATH = "data3.db"
EMAIL_DOMAIN = "test.ru"
WRITING_MUTEX = threading.Lock()

def connect():
    return sqlite3.connect(DB_PATH)



def registerDB():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Mail(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme TEXT,
    content TEXT,
    author INTEGER,
    sentTo INTEGER
    )
    ''')#Таблица с почтой
    connection.commit()


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
    )
    ''')#Таблица с пользователями
    connection.commit()



def create_email(email, hashedPassword):
    if "@" not in email:
        error = f"{email} не соответсвует правилам формата"
        print(error)
        return (False,error)

    input_domain = email.split("@")[1]
    if(input_domain != EMAIL_DOMAIN):
        error = f"{email} не соответсвует название домена"
        print(error)
        return (False,error)
    with WRITING_MUTEX:
        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO Users (email,password) 
                VALUES (?,?)
            ''', (email,hashedPassword))
            connection.commit()
            success = f"Пользователь {email} был успешно создан"
            print(success)
            return (True,success)
        except sqlite3.Error as e:
            error = f"Ошибка при создании пользователя: {e}"
            print(error)
            return (False,error)




def check_email_exists(email):
    cursor = connect().cursor()
    cursor.execute('''
    SELECT * FROM Users WHERE email = ?
    ''', (email,))
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
    with WRITING_MUTEX:
        try:
            connection = connect()
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO Mail (theme,content,author,sentTo) 
                VALUES (?,?,?,?)
            ''', (theme,content,author_id,sent_to_id))
            connection.commit()
            success = f"Письмо от {author_id} до {sent_to_id} было успешно добавлено"
            print(success)
            return (True,success)
        except sqlite3.Error as e:
            error = f"Ошибка при добавлении письма {e}"
            print(error)
            return (False,error)




def get_mail_for_email(email,password):
    user = check_email_exists(email)
    print(user)
    print(password)
    if(user[1] == None or user[1][2] != password):
        return(False,"Пользователь не найден")
    userID = user[1][0]
    print("ID = ",userID)
    cursor = connect().cursor()
    cursor.execute('''
        SELECT * FROM Mail WHERE author = ?
    ''', (userID,))
    data = cursor.fetchall()
    return(True,data)



def close(connection):
    connection.close()