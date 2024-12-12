import json

class User:
    def __init__(self, id = None, email=None):
        self.id = id
        self.email = email

    def toString(self):
        return json.dumps(
        {
            "id":self.id,
            "email":self.email
        })

class Mail:
    def __init__(self, id=None, theme=None, content=None, author_id=None, sent_to_id=None):
        self.id = id
        self.theme = theme
        self.content = content
        self.author_id = author_id
        self.sent_to_id = sent_to_id

    def toString(self):
        return json.dumps(
        {
            "id":self.id,
            "theme":self.theme,
            "content":self.content,
            "authorID":self.author_id,
            "sentToId":self.sent_to_id
        })
    def toJson(self):
        return {
            "id":self.id,
            "theme":self.theme,
            "content":self.content,
            "authorID":self.author_id,
            "sentToId":self.sent_to_id
        }