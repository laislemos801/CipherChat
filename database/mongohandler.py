import base64
import datetime
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from utils import clear_terminal, carregar

# Conectar ao banco de dados
client = MongoClient(
    'mongodb+srv://laispl2:qwerty123456@consultas.hihh4wp.mongodb.net/?retryWrites=true&w=majority&appName=Consultas'
)
db = client["CipherChat"]
db_users = db.users
db_messages = db.messages

class MongoHandler:
    def xor_crypt(self, message, key):
        if not key:
            print("🔴 Erro: A chave de criptografia não está definida.")
            return None
        encrypted_bytes = bytes(
            ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(message)
        )
        encrypted_message = base64.b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_message

    def xor_decrypt(self, encrypted_message, key):
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

    def enviar_mensagem(self, usuario):  # Adicione 'self' aqui
        load_dotenv()
        key = os.getenv('KEY_CRYPTO')

        if not key:
            print("🔴 Erro: A chave de criptografia não está definida. Configure a variável de ambiente 'KEY_CRYPTO'.")
            return

        try:
            usuarios_cadastrados = list(db_users.find({}, {"username": 2, "_id": 0}))
        except PyMongoError as e:
            print(f"🔴 Erro ao acessar o banco de dados: {e}")
            return

        if not usuarios_cadastrados:
            print("🔴 Nenhum usuário cadastrado encontrado.")
            return

        clear_terminal()
        print("=" * 39)
        print("📬 Escolha o destinatário da mensagem:")
        print("=" * 39)
        for idx, user in enumerate(usuarios_cadastrados, start=1):
            print(f"{idx}) {user['username']}")

        while True:
            try:
                escolha = int(input("\n🔍 Escolha o número do destinatário: "))
                if 1 <= escolha <= len(usuarios_cadastrados):
                    destinatario = usuarios_cadastrados[escolha - 1]['username']
                    break
                else:
                    print("🔴 Opção inválida, escolha um número válido.")
            except ValueError:
                print("🔴 Entrada inválida, digite um número.")

        mensagem = input("💬 Digite sua mensagem: ")
        encrypted_message = self.xor_crypt(mensagem, key)  # Usando 'self'
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

    def ler_mensagens(self, usuario):  # Adicione 'self' aqui
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
                    decrypted_message = self.xor_decrypt(msg['mensagem'], key)  # Usando 'self'
                    data_formatada = msg['data'].strftime('%d/%m/%Y %H:%M:%S')

                    # Formatação personalizada como e-mail
                    print("=" * 50)
                    if decrypted_message is None:
                        print(
                            f"🔴 De: {msg['remetente']}\nEnviado: {data_formatada}\n\nMensagem: [Erro na descriptografia]")
                    else:
                        print(f"🔹 De: {msg['remetente']}\nEnviado: {data_formatada}\n\nMensagem:\n{decrypted_message}")
                    print("=" * 50)

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
