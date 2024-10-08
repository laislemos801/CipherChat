import datetime as datetime


class User:
    def __init__(self, username: str, name: str, email: str, password: str):
        '''
        Constuctor of User object
        :param username: the username and nickname are same.
        :param name: complete name of User
        :param email: email of user
        :param password: :-)
        '''
        self.username = username
        self.name = name
        self.email = email
        self.password = password


class Message:
    def __init__(self, username_from: str, username_to: str, text_content: str,
                 date: datetime.datetime):
        '''
        :param username_from:
        :param username_to:
        :param text_content:
        :param date:
        '''
        self.username_from = username_from
        self.username_to = username_to
        self.text_content = text_content
        self.datetime = date
