# main.py
import os
import sys

# Verifica se os módulos necessários estão presentes
try:
    import tkinter as tk
    import mysql.connector
    from login_mysql import login_bd
except ImportError as e:
    print("Erro de importação:", e)
    sys.exit(1)

def iniciar_sistema():
    try:
        login_bd()  # Chama a função principal da tela de login do BD
    except Exception as e:
        print("Erro ao iniciar o sistema:", e)

if __name__ == "__main__":
    iniciar_sistema()
