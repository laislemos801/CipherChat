import re
import datetime
from pymongo import MongoClient

# Função para conectar ao banco de dados e retornar a coleção de usuários
def connect_db():
    client = MongoClient(
        'mongodb+srv://ana:ana39@consultas.2opj3.mongodb.net/?retryWrites=true&w=majority&appName=Consultas'
    )
    db = client["aulapython"]
    return db.users  # Retorna a coleção de usuários

# Função que valida a senha
def validar_senha(password):
    match password:
        case pw if len(pw) < 8:
            print("A senha deve ter pelo menos 8 caracteres.")
            return False
        case pw if not re.search(r"[A-Z]", pw):
            print("A senha deve conter pelo menos uma letra maiúscula.")
            return False
        case pw if not re.search(r"[a-z]", pw):
            print("A senha deve conter pelo menos uma letra minúscula.")
            return False
        case pw if not re.search(r"\d", pw):
            print("A senha deve conter pelo menos um número.")
            return False
        case pw if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
            print("A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?\":{}|<>).")
            return False
        case _:
            return True  # Se todas as condições forem atendidas, a senha é válida.

# Função de cadastro que verifica usuário e senha
def cadastro():
    db_users = connect_db()

    #Solicita o email e senha
    email = input("Digite seu e-mail: ")
    password = input("Digite sua senha: ")

    # Verifica se o e-mail já está cadastrado
    if db_users.find_one({"email": email}):
        print("E-mail já cadastrado. Tente novamente.")
        return False

    # Valida a senha
    if not validar_senha(password):
        return False

    # Cria um documento para o novo usuário
    novo_usuario = {
        "email": email,
        "password": password,
        "created_at": datetime.datetime.now(tz=datetime.timezone.utc)
    }

    # Insere o usuário no banco de dados
    db_users.insert_one(novo_usuario)
    return True

def login ():
   db_users = connect_db()

   # Solicita o email e senha
   email = input("Digite seu e-mail: ")
   password = input("Digite sua senha: ")

   if db_users.find_one({"email": email, "password": password}):
       return True
   else:
        return False

# Função principal
def main():

    print("Bem-vindo ao CipherChat!")
    while True:
        option = input("Você deseja (1) cadastrar | (2) fazer login? | (3) Sair do programa: ")
        if option == "1":
            print("Cadastre-se")
            if cadastro():
                print("Usuário cadastrado com sucesso!")
            else:
                print("Erro no cadastro.")
        elif option == "2":
            print("Login")
            if login():
                print("Login realizado com sucesso!")
            else:
                print("Erro no login.")

        elif option == "3":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")



if __name__ == '__main__':
    main()
