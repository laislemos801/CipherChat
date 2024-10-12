# Projeto CipherChat

## Integrantes: 
- Ana Carolina Morelli Chaves – 23017617
- Lais de Paula Lemos – 23016041
- Luiz Gustavo Pinto da Silva - 23013028

Olá! Segue o tutorial de instalação do projeto para que tudo funcione corretamente.

1) Após baixar o .zip e abrir o projeto no PyCharm (python versão 3.12), é preciso instalar os pacotes. Use esses comandos no terminal:
    ```bash
    pip install pymongo
    pip install "pymongo[gssapi,ocsp,snappy,zstd,encryption]"
    pip install aes-pkcs5
    ```

2) Faça a instalação dos requirements escrevendo no terminal:
    ```bash
    pip install -r requirements.txt
    ```

3) Se quiser, fique à vontade para mudar a string de conexão com o banco MongoDB Atlas, e verificar o funcionamento da criptografia. Deve ser mudado nos arquivos `main.py` e `mongohandler.py`.

4) Por fim, só rodar o programa e enviar suas mensagens criptografadas!