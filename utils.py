import os
import time

# Função para limpar o terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função de carregamento
def carregar():
    print("🔄 Carregando", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print("\n")
    clear_terminal()
