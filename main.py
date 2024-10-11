import re
import datetime
from pymongo import MongoClient

# Conectar ao banco de dados uma única vez
client = MongoClient(
    'mongodb+srv://ana:ana39@consultas.2opj3.mongodb.net/?retryWrites=true&w=majority&appName=Consultas'
)
db = client["aulapython"]
db_users = db.users  # Coleção de usuários
db_messages = db.messages  # Coleção de mensagens

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
    # Solicita o email
    email = input("Digite seu e-mail: ")

    # Verifica se o e-mail já está cadastrado
    if db_users.find_one({"email": email}):
        print("E-mail já cadastrado. Tente novamente.")
        return False

    # Loop para solicitar a senha até que ela seja válida
    while True:
        password = input("Digite sua senha: ")
        if validar_senha(password):
            break  # Sai do loop se a senha for válida
        else:
            print("Tente novamente.")

    # Cria um documento para o novo usuário
    novo_usuario = {
        "email": email,
        "password": password,
        "created_at": datetime.datetime.now(tz=datetime.timezone.utc)
    }

    # Insere o usuário no banco de dados
    db_users.insert_one(novo_usuario)
    return True

# Função de login
def login():
    # Solicita o email e senha
    email = input("Digite seu e-mail: ")
    password = input("Digite sua senha: ")

    if db_users.find_one({"email": email, "password": password}):
        return email  # Retorna o e-mail do usuário logado
    else:
        return None

# Função para enviar uma mensagem
def enviar_mensagem(usuario):
    # Recupera todos os usuários cadastrados no banco de dados
    usuarios_cadastrados = list(db_users.find({}, {"email": 1, "_id": 0}))  # Retorna apenas os e-mails

    if not usuarios_cadastrados:
        print("Nenhum usuário cadastrado encontrado.")
        return

    # Exibe os usuários cadastrados com numeração
    print("Usuários cadastrados:")
    for idx, user in enumerate(usuarios_cadastrados, start=1):
        print(f"{idx}) {user['email']}")

    # Solicita que o remetente escolha o destinatário pela numeração
    while True:
        try:
            escolha = int(input("Escolha o número do destinatário: "))
            if 1 <= escolha <= len(usuarios_cadastrados):
                destinatario = usuarios_cadastrados[escolha - 1]['email']
                break
            else:
                print("Opção inválida, escolha um número válido.")
        except ValueError:
            print("Entrada inválida, digite um número.")

    # Solicita a mensagem
    mensagem = input("Digite sua mensagem: ")

    # Cria um documento de mensagem
    nova_mensagem = {
        "remetente": usuario,
        "destinatario": destinatario,
        "mensagem": mensagem,
        "data": datetime.datetime.now(tz=datetime.timezone.utc)
    }

    # Insere a mensagem no banco de dados
    db_messages.insert_one(nova_mensagem)
    print(f"Mensagem enviada com sucesso para {destinatario}!")


# Função para ler mensagens
def ler_mensagens(usuario):
    mensagens = db_messages.find({"destinatario": usuario})

    if mensagens.count() == 0:
        print("Nenhuma mensagem encontrada.")
    else:
        for msg in mensagens:
            print(f"De: {msg['remetente']}, Mensagem: {msg['mensagem']}")

# Função que exibe o menu após login bem-sucedido
def menu_usuario(usuario):
    while True:
        print("\nEscolha uma opcao:")
        print("(1) Enviar mensagem")
        print("(2) Ler mensagens")
        print("(3) Sair")
        option = input("Escolha uma opção: ")

        if option == "1":
            enviar_mensagem(usuario)
        elif option == "2":
            ler_mensagens(usuario)
        elif option == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Função principal
def main():
    print("Bem-vindo ao CipherChat!")
    while True:
        print("\nVocê deseja:")
        print("(1) Fazer cadastro")
        print("(2) Fazer login")
        print("(3) Sair do programa")
        option = input("Escolha uma opção: ")

        if option == "1":
            print("Cadastre-se")
            if cadastro():
                print("Usuário cadastrado com sucesso!")
            else:
                print("Erro no cadastro.")
        elif option == "2":
            print("Login")
            usuario = login()
            if usuario:
                print("Login realizado com sucesso!")
                menu_usuario(usuario)  # Mostra o menu após login
            else:
                print("Erro no login.")
        elif option == "3":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
