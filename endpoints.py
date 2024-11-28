import models
import headers
import json
import endpoint_utils as eu
import database as db
EMAIL_KEY = "email"

def echo(self):

    content_length = eu.get_content_length(self)
    query_params = eu.parse_get_data(self)

    print(f"Получено сообщение: {query_params}")
    headers.response(self,200,json.dumps(query_params).encode())

def create_email(self):
    content_length = eu.get_content_length(self)
    query_params = eu.parse_get_data(self)
    resp = db.create_email(query_params[EMAIL_KEY][0])[1]

    print(f"Получено сообщение: {query_params}")
    headers.response(self,200,resp.encode())


def check_email_exists(self):
    content_length = eu.get_content_length(self)
    query_params = eu.parse_get_data(self)
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
    query_params = eu.parse_get_data(self)

    print(f"Получено сообщение: {query_params}")

    author = db.check_email_exists(query_params[AUTHOR_KEY][0])[1]
    if(author == None):
        headers.response(self,200,"Автора письма не существует".encode())
        return
        #author = models.User(author[0],author[1]).toString()
    
    target = db.check_email_exists(query_params[TARGET_KEY][0])[1]
    if(target == None):
        headers.response(self,200,"Цели для отправки письма не существует".encode())
        return
        #target = models.User(author[0],author[1]).toString()
    
    content = query_params[CONTENT_KEY][0]
    theme = query_params[THEME_KEY][0]

    resp = db.send_mail(theme,content,author[0],target[0])
    headers.response(self,200,resp[1].encode())

def read_mail(self):
    RECIEVER_KEY = "reciever"
    content_length = eu.get_content_length(self)
    query_params = eu.parse_get_data(self)

    print(f"Получено сообщение: {query_params}")
    result = db.get_mail_for_email(query_params[RECIEVER_KEY][0])
    print(result)
    mails = {}
    for i in range(len(result)):
        i_res = result[1][i]
        mails[i] = (models.Mail(i_res[0],i_res[1],i_res[2],i_res[3],i_res[4])).toString() + "\n"
    

    headers.response(self,200,json.dumps(mails).encode())
