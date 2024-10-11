import re
import datetime

from dotenv import load_dotenv
from pymongo import MongoClient
import os
import base64
from pymongo.errors import PyMongoError
import time

# Conectar ao banco de dados uma única vez
client = MongoClient(
    'mongodb+srv://laispl2:qwerty123456@consultas.hihh4wp.mongodb.net/?retryWrites=true&w=majority&appName=Consultas'
)
db = client["aulapython"]
db_users = db.users  # Coleção de usuários
db_messages = db.messages  # Coleção de mensagens

# Função para limpar o terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

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
            carregar()  # Chama a função de carregamento após o login
            clear_terminal()
            print("🔴 A senha deve ter pelo menos 8 caracteres.")
            return False
        case pw if not re.search(r"[A-Z]", pw):
            carregar()  # Chama a função de carregamento após o login
            clear_terminal()
            print("🔴 A senha deve conter pelo menos uma letra maiúscula.")
            return False
        case pw if not re.search(r"[a-z]", pw):
            carregar()  # Chama a função de carregamento após o login
            clear_terminal()
            print("🔴 A senha deve conter pelo menos uma letra minúscula.")
            return False
        case pw if not re.search(r"\d", pw):
            carregar()  # Chama a função de carregamento após o login
            clear_terminal()
            print("🔴 A senha deve conter pelo menos um número.")
            return False
        case pw if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
            carregar()  # Chama a função de carregamento após o login
            clear_terminal()
            print("🔴 A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?\":{}|<>).")
            return False
        case _:
            return True  # Se todas as condições forem atendidas, a senha é válida.


# Função de cadastro que verifica usuário e senha
def cadastro():
    email = input("✉️ Digite seu e-mail: ")

    if not validar_email(email):
        carregar()  # Chama a função de carregamento após o login
        clear_terminal()
        print("🔴 E-mail inválido. Tente novamente.")
        return False

    if db_users.find_one({"email": email}):
        carregar()  # Chama a função de carregamento após o login
        clear_terminal()
        print("🔴 E-mail já cadastrado. Tente novamente.")
        return False

    while True:
        username = input("👤 Escolha um nome de usuário (sem espaços): ")

        if validar_username(username):
            if db_users.find_one({"username": username}):
                carregar()  # Chama a função de carregamento após o login
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
        if db_users.find_one({"email": email, "password": password}):
            return email
        else:
            carregar()  # Chama a função de carregamento após o login
            clear_terminal()
            print("🔴 E-mail ou senha incorretos.")
            return None
    except PyMongoError as e:
        carregar()  # Chama a função de carregamento após o login
        clear_terminal()
        print(f"🔴 Erro ao acessar o banco de dados: {e}")
        return None

def xor_crypt(message, key):
    if not key:
        print("🔴 Erro: A chave de criptografia não está definida.")
        return None
    encrypted_bytes = bytes(
        ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(message)
    )
    encrypted_message = base64.b64encode(encrypted_bytes).decode('utf-8')
    return encrypted_message

def xor_decrypt(encrypted_message, key):
    if not key:
        print("🔴 Erro: A chave de criptografia não está definida.")
        return None
    try:
        encrypted_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
    except base64.binascii.Error:
        print("🔴 Erro: Mensagem criptografada em formato inválido.")
        return None
    decrypted_message = ''.join(
        chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(encrypted_bytes)
    )
    return decrypted_message

def enviar_mensagem(usuario):
    load_dotenv()
    key = os.getenv('KEY_CRYPTO')

    if not key:
        print("🔴 Erro: A chave de criptografia não está definida. Configure a variável de ambiente 'KEY_CRYPTO'.")
        return

    try:
        usuarios_cadastrados = list(db_users.find({}, {"email": 1, "_id": 0}))
    except PyMongoError as e:
        print(f"🔴 Erro ao acessar o banco de dados: {e}")
        return

    if not usuarios_cadastrados:
        print("🔴 Nenhum usuário cadastrado encontrado.")
        return

    clear_terminal()
    print("="*39)
    print("📬 Escolha o destinatário da mensagem:")
    print("="*39)
    for idx, user in enumerate(usuarios_cadastrados, start=1):
        print(f"{idx}) {user['email']}")

    while True:
        try:
            escolha = int(input("\n🔍 Escolha o número do destinatário: "))
            if 1 <= escolha <= len(usuarios_cadastrados):
                destinatario = usuarios_cadastrados[escolha - 1]['email']
                break
            else:
                print("🔴 Opção inválida, escolha um número válido.")
        except ValueError:
            print("🔴 Entrada inválida, digite um número.")

    mensagem = input("💬 Digite sua mensagem: ")
    encrypted_message = xor_crypt(mensagem, key)
    if encrypted_message is None:
        print("🔴 Falha na criptografia da mensagem.")
        return

    nova_mensagem = {
        "remetente": usuario,
        "destinatario": destinatario,
        "mensagem": encrypted_message,
        "data": datetime.datetime.now(tz=datetime.timezone.utc)
    }

    try:
        db_messages.insert_one(nova_mensagem)
        clear_terminal()
        carregar()
        print(f"✅ Mensagem enviada com sucesso para {destinatario}!")
    except PyMongoError as e:
        print(f"🔴 Erro ao enviar mensagem: {e}")

def ler_mensagens(usuario):
    load_dotenv()
    key = os.getenv('KEY_CRYPTO')

    if not key:
        print("🔴 Erro: A chave de criptografia não está definida. Configure a variável de ambiente 'KEY_CRYPTO'.")
        return

    try:
        count = db_messages.count_documents({"destinatario": usuario})
    except PyMongoError as e:
        print(f"🔴 Erro ao acessar o banco de dados: {e}")
        return

    if count == 0:
        print("🔴 Nenhuma mensagem encontrada.")
    else:
        try:
            mensagens = db_messages.find({"destinatario": usuario})
            clear_terminal()
            print("\n📥 Mensagens recebidas:")
            for msg in mensagens:
                decrypted_message = xor_decrypt(msg['mensagem'], key)
                data_formatada = msg['data'].strftime('%d/%m/%Y %H:%M:%S')
                
                # Formatação personalizada como e-mail
                print("="*50)
                if decrypted_message is None:
                    print(f"🔴 De: {msg['remetente']}\nEnviado: {data_formatada}\n\nMensagem: [Erro na descriptografia]")
                else:
                    print(f"🔹 De: {msg['remetente']}\nEnviado: {data_formatada}\n\nMensagem:\n{decrypted_message}")
                print("="*50)

        except PyMongoError as e:
            print(f"🔴 Erro ao recuperar mensagens: {e}")

    # Pergunta ao usuário se deseja sair
    while True:
        print("\nVocê deseja fechar as mensagens?")
        escolha = input("Digite 1 para fechar: ")
        if escolha == "1":
            clear_terminal()
            print("👋 Fechando mensagens...")
            return  # Sai da função
        else:
            print("🔴 Opção inválida. Tente novamente.")

# Função de carregamento
def carregar():
    print("🔄 Carregando", end="")
    for _ in range(3):  # Exibe por 3 segundos
        print(".", end="", flush=True)
        time.sleep(1)
    print("\n")
    clear_terminal()

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
            enviar_mensagem(usuario)
        elif option == "2":
            ler_mensagens(usuario)
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
                carregar()  # Chama a função de carregamento após o cadastro
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
                carregar()  # Chama a função de carregamento após o login
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
