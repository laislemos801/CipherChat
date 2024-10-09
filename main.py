from pymongo import MongoClient
import datetime
from database import mongohandler
from database.entities import User, Message

# Função para conectar ao banco de dados e inserir um documento
def connect_and_put_single_doc():
    post = {
        "author": "Lais",
        "text": "mensagem criptografada",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    client = MongoClient(
        'mongodb+srv://laispl2:qwerty123456@consultas.hihh4wp.mongodb.net/?retryWrites=true&w=majority&appName=Consultas'
    )
    db = client["aulapython"]
    col_docs = db.docs
    id_res = col_docs.insert_one(post).inserted_id
    return id_res

# Função de login que verifica usuário e senha
def login(email, password):
    # Aqui você pode colocar a lógica de autenticação, como verificar o banco de dados
    # Exemplo simples de verificação
    if email == 'laisaplemos10@gmail.com' and password == '123':
        print(f"Usuário {email} autenticado com sucesso!")
        return True
    else:
        print("Falha na autenticação.")
        return False

# Função principal
def main():
    # Exemplo de criação de usuário e mensagem
    my_user = User(email='laisaplemos10@gmail.com', password='123', username='Lais', name='Lais Lemos')
    print(f"E-mail do usuário: {my_user.email}")

    my_message = Message("Lais", "Ana", "texto...", datetime.datetime.now(tz=datetime.timezone.utc))
    mongohandler.add_new_message(my_message)

    # Chama a função de login
    email = input("Digite seu e-mail: ")
    password = input("Digite sua senha: ")
    if login(email, password):
        print("Login realizado com sucesso!")
    else:
        print("Erro no login.")

if __name__ == '__main__':
    main()
