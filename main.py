import re
import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from database.mongohandler import MongoHandler
from utils import clear_terminal, carregar

# Conectar ao banco de dados
client = MongoClient(
    'mongodb+srv://laispl2:qwerty123456@consultas.hihh4wp.mongodb.net/?retryWrites=true&w=majority&appName=Consultas'
)
db = client["CipherChat"]
db_users = db.users
db_messages = db.messages

#importando MongoHandler
obj = MongoHandler()

# Função para validar e-mail
def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Função para validar o nome de usuário
def validar_username(username):
    # Verifica se o username contém apenas letras, números, sublinhos e hífens
    return re.match(r"^[a-zA-Z0-9_-]+$", username) is not None

# Função que valida a senha
def validar_senha(password):
    match password:
        case pw if len(pw) < 8:
            carregar()  # Chama a função de carregamento
            clear_terminal()
            print("🔴 A senha deve ter pelo menos 8 caracteres.")
            return False
        case pw if not re.search(r"[A-Z]", pw):
            carregar()
            clear_terminal()
            print("🔴 A senha deve conter pelo menos uma letra maiúscula.")
            return False
        case pw if not re.search(r"[a-z]", pw):
            carregar()
            clear_terminal()
            print("🔴 A senha deve conter pelo menos uma letra minúscula.")
            return False
        case pw if not re.search(r"\d", pw):
            carregar()
            clear_terminal()
            print("🔴 A senha deve conter pelo menos um número.")
            return False
        case pw if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
            carregar()
            clear_terminal()
            print("🔴 A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?\":{}|<>).")
            return False
        case _:
            return True

# Função de cadastro que verifica usuário e senha
def cadastro():
    email = input("✉️ Digite seu e-mail: ")

    if not validar_email(email):
        carregar()
        clear_terminal()
        print("🔴 E-mail inválido. Tente novamente.")
        return False

    if db_users.find_one({"email": email}):
        carregar()
        clear_terminal()
        print("🔴 E-mail já cadastrado. Tente novamente.")
        return False

    while True:
        username = input("👤 Escolha um nome de usuário (sem espaços): ")

        if validar_username(username):
            if db_users.find_one({"username": username}):
                carregar()
                clear_terminal()
                print("🔴 Nome de usuário já cadastrado. Tente novamente.")
            else:
                break
        else:
            print("🔴 Nome de usuário inválido. Use apenas letras, números, sublinhos ou hífens e sem espaços.")

    while True:
        password = input("🔒 Digite sua senha: ")
        if validar_senha(password):
            break
        else:
            print("🔴 Tente novamente.")

    novo_usuario = {
        "email": email,
        "username": username,  # Adiciona o campo username
        "password": password,
        "created_at": datetime.datetime.now(tz=datetime.timezone.utc)
    }

    try:
        db_users.insert_one(novo_usuario)
        return True
    except PyMongoError as e:
        print(f"🔴 Erro ao inserir usuário no banco de dados: {e}")
        return False

# Função de login
def login():
    email = input("✉️ Digite seu e-mail: ")
    password = input("🔒 Digite sua senha: ")

    try:
        # Busca o usuário pelo email e senha
        user = db_users.find_one({"email": email, "password": password})
        if user:
            # Retorna o username do documento encontrado
            return user['username']
        else:
            carregar()
            clear_terminal()
            print("🔴 E-mail ou senha incorretos.")
            return None
    except PyMongoError as e:
        carregar()
        clear_terminal()
        print(f"🔴 Erro ao acessar o banco de dados: {e}")
        return None

# Função que exibe o menu após login bem-sucedido
def menu_usuario(usuario):
    while True:
        print("\n" + "="*30)
        print(" "*8 + "MENU DE USUÁRIO")
        print("="*30)
        print(" "*4 + "(1) Enviar mensagem")
        print(" "*4 + "(2) Ler mensagens")
        print(" "*4 + "(3) Sair")
        print("="*30)
        option = input("Escolha uma opção: ")

        if option == "1":
            obj.enviar_mensagem(usuario)
        elif option == "2":
            obj.ler_mensagens(usuario)
        elif option == "3":
            clear_terminal()
            print("👋 Saindo...")
            break
        else:
            print("🔴 Opção inválida. Tente novamente.")

# Função principal
def main():
    clear_terminal()
    print("="*30)
    print(" "*3 + "BEM-VINDO AO CIPHERCHAT!")
    print("="*30)
    while True:
        print("\n" + "="*30)
        print(" "*8 + "MENU PRINCIPAL")
        print("="*30)
        print(" "*4 + "(1) Fazer cadastro")
        print(" "*4 + "(2) Fazer login")
        print(" "*4 + "(3) Sair do programa")
        print("="*30)
        option = input("Escolha uma opção: ")

        if option == "1":
            clear_terminal()
            print("\n" + "="*30)
            print(" "*8 +"📝 CADASTRE-SE")
            print("="*30)
            if cadastro():
                carregar()
                print("✅ Usuário cadastrado com sucesso!")
            else:
                print("🔴 Erro no cadastro.")
        elif option == "2":
            clear_terminal()
            print("\n" + "="*30)
            print(" "*10 +"🔑 LOGIN")
            print("="*30)
            usuario = login()
            if usuario:
                carregar()
                print("✅ Login realizado com sucesso!")
                menu_usuario(usuario)
            else:
                print("🔴 Erro no login.")
        elif option == "3":
            clear_terminal()
            print("👋 Saindo do programa...")
            break  # Sai do loop principal e encerra o programa
        else:
            print("🔴 Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
