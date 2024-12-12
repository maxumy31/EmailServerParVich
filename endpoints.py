import models
import headers
import json
import endpoint_utils as eu
import database as db
EMAIL_KEY = "email"
PASSWORD_KEY = "password"

def echo(self):

    content_length = eu.get_content_length(self)
    query_params = eu.parse_get_data(self)

    print(f"Получено сообщение: {query_params}")
    headers.response(self,200,json.dumps(query_params).encode())



def create_email(self):
    content_length = eu.get_content_length(self)
    query_params = eu.parse_post_data(self, content_length)
    print(query_params)
    password = query_params.get(PASSWORD_KEY)
    email = query_params.get(EMAIL_KEY)
    if not password or not email:
        print("wrong request body")
        headers.response(self,400,"".encode())
        return
    print(password)
    password = eu.hash_password(password)
    exists = db.check_email_exists(email)
    if exists[0]:
        print("User already exists")
        headers.response(self,400,"".encode())
        return
    resp = db.create_email(email,password)[1]
    print(resp)

    print(f"Получено сообщение: {query_params}")
    headers.response(self,200,resp.encode())




def check_email_exists(self):
    content_length = eu.get_content_length(self)
    query_params = eu.parse_get_data(self)
    email = query_params.get(EMAIL_KEY)
    if not email:
        print("wrong request")
        headers.response(self,400,"".encode())  
    resp = db.check_email_exists(query_params[EMAIL_KEY][0])[1]

    print(f"Получено сообщение: {query_params}")
    print(resp)
    if(resp == None):
        resp = ""
    else:
        resp = (models.User(resp[0],resp[1])).toString()
    print(resp)
    
    headers.response(self,200,resp.encode())



def send_mail(self):
    AUTHOR_KEY = "author"
    TARGET_KEY = "target"
    CONTENT_KEY = "content"
    THEME_KEY = "theme"
    content_length = eu.get_content_length(self)
    query_params = eu.parse_post_data(self,content_length)

    print(f"Получено сообщение: {query_params}")
    print(query_params[AUTHOR_KEY])

    author = db.check_email_exists(query_params[AUTHOR_KEY])[1]
    if(author == None):
        headers.response(self,200,"Автора письма не существует".encode())
        return

    password = eu.hash_password(query_params[PASSWORD_KEY])
    if(password != author[2]):
        headers.response(self,200,"Указан неверный пароль".encode())
        return
    
    target = db.check_email_exists(query_params[TARGET_KEY])[1]
    if(target == None):
        headers.response(self,200,"Цели для отправки письма не существует".encode())
        return
    
    content = query_params[CONTENT_KEY]
    theme = query_params[THEME_KEY]

    resp = db.send_mail(theme,content,author[0],target[0])
    headers.response(self,200,resp[1].encode())

def read_mail(self):
    RECIEVER_KEY = "reciever"
    content_length = eu.get_content_length(self)
    query_params = eu.parse_post_data(self,content_length)

    password = query_params.get(PASSWORD_KEY)
    if not password:
        headers.response(self,200,"Указан неверный пароль".encode())
        return
    
    password = eu.hash_password(password[0])
    reciever = query_params.get(RECIEVER_KEY)
    if not reciever:
        headers.response(self,200,"Указан неверный пароль".encode())
        return

    print(f"Получено сообщение: {query_params}")
    result = db.get_mail_for_email(reciever,password)

    if(result[0] == False):
        headers.response(self,500,"Пользователь не найден".encode())
        return

    mails = []
    for i in range(len(result[1])):
        i_res = result[1][i]
        print(i_res)
        mails.append((models.Mail(i_res[0],i_res[1],i_res[2],i_res[3],i_res[4])).toJson())

    

    headers.response(self,200,json.dumps(mails).encode())
