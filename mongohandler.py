from database.entities import *


def add_new_message(m: Message): #Message é do arquivo models, estamos omitindo models.Message
    d = m.__dict__
    print(d)