# login_mysql.py
import tkinter as tk
from tkinter import messagebox
from db_config import conectar_bd

def abrir_login_sistema(conexao):
    # Aqui você importaria e chamaria a próxima tela
    messagebox.showinfo("Sucesso", "Conexão estabelecida com sucesso!")
    # Exemplo: login_sistema.abrir(conexao)

def login_bd():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    conexao = conectar_bd(usuario, senha)

    if conexao:
        root.destroy()  # fecha a janela de login do BD
        abrir_login_sistema(conexao)
    else:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados.\nVerifique as credenciais.")

# ----- Interface gráfica -----
root = tk.Tk()
root.title("Login - Banco de Dados UniUFC-BD")
root.geometry("350x200")
root.resizable(False, False)

tk.Label(root, text="Usuário MySQL:").pack(pady=(20, 0))
entry_usuario = tk.Entry(root)
entry_usuario.pack()

tk.Label(root, text="Senha MySQL:").pack()
entry_senha = tk.Entry(root, show="*")
entry_senha.pack()

btn_login = tk.Button(root, text="Conectar", command=login_bd)
btn_login.pack(pady=15)

root.mainloop()

