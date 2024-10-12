import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from utils import clear_terminal, carregar
from aes_pkcs5.algorithms.aes_cbc_pkcs5_padding import AESCBCPKCS5Padding

# Conectar ao banco de dados
client = MongoClient(
    'mongodb+srv://laispl2:qwerty123456@consultas.hihh4wp.mongodb.net/?retryWrites=true&w=majority&appName=Consultas'
)
db = client["CipherChat"]
db_users = db.users
db_messages = db.messages

class MongoHandler:
    def xor_crypt(self, message, key, iv_parameter="0011223344556677", output_format="b64"):

        keyB= key.ljust(16, '0')[:16]  # muda o tamamho

        cipher=AESCBCPKCS5Padding(keyB, output_format, iv_parameter)
        encrypted_message=cipher.encrypt(message)
        return encrypted_message

    def xor_decrypt(self, encrypted_message, key, iv_parameter="0011223344556677", output_format="b64"):
        keyB = key.ljust(16, '0')[:16]  # muda o tamamho
        cipher = AESCBCPKCS5Padding(keyB, output_format, iv_parameter)
        decrypt_message = cipher.decrypt(encrypted_message)
        return decrypt_message

    def enviar_mensagem(self, usuario):

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
        if not mensagem.strip():
            print("🔴 A mensagem não pode estar vazia.")
            return

        # Solicita a chave após escolher o destinatário
        key = input("🔑 Digite a chave de criptografia: ")
        key = key.ljust(16, '0')[:16]  # Ajusta o tamanho da chave

        encrypted_message = self.xor_crypt(mensagem, key)
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

    def ler_mensagens(self, usuario):
        try:
            mensagens_enviadas = list(db_messages.find({"destinatario": usuario}))
        except PyMongoError as e:
            print(f"🔴 Erro ao acessar o banco de dados: {e}")
            return

        if not mensagens_enviadas:
            print("🔴 Nenhuma mensagem encontrada.")
            return

        clear_terminal()
        print("=" * 39)
        print("📬 Mensagens recebidas:")
        print("=" * 39)

        # Exibe as mensagens e os remetentes
        for idx, mensagem in enumerate(mensagens_enviadas, start=1):
            print(f"{idx}) De: {mensagem['remetente']} | Data: {mensagem['data']}")

        while True:
            try:
                escolha = int(input("\n🔍 Escolha o número da mensagem para ler: "))
                if 1 <= escolha <= len(mensagens_enviadas):
                    mensagem_selecionada = mensagens_enviadas[escolha - 1]
                    break
                else:
                    print("🔴 Opção inválida, escolha um número válido.")
            except ValueError:
                print("🔴 Entrada inválida, digite um número.")

        # Solicita a chave para descriptografar a mensagem
        key = input("🔑 Digite a chave de criptografia: ")

        # Descriptografa a mensagem
        try:
            decrypted_message = self.xor_decrypt(mensagem_selecionada['mensagem'], key)

            # Verifica se a mensagem descriptografada é válida
            if not decrypted_message:
                print("🔴 Chave de criptografia inválida. Não foi possível descriptografar a mensagem.")
            else:
                print(f"\n💬 Mensagem: {decrypted_message}")  # Exibe a mensagem descriptografada
        except Exception as e:
            print(f"🔴 Erro ao descriptografar a mensagem: {e}")
