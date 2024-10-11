
import base64



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

