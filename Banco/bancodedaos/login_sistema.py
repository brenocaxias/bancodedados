# login_sistema.py
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from telaprincipal import menu_principal

def abrir_menu_principal(tipo_usuario, nome_usuario):
    menu_principal(tipo_usuario,nome_usuario,conexao)
    messagebox.showinfo("Bem-vindo", f"Acesso concedido a {nome_usuario} ({tipo_usuario})")
    # Exemplo: menu_principal.abrir(tipo_usuario, nome_usuario, conexao)

def login_sistema(conexao):
    def autenticar():
        login = entry_login.get()
        senha = entry_senha.get()

        try:
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE login = %s AND senha = %s"
            cursor.execute(query, (login, senha))
            usuario = cursor.fetchone()

            if usuario:
                root.destroy()
                abrir_menu_principal(usuario['tipo'], usuario['nome'])
            else:
                # Verifica se é o Admin padrão
                if login == "Admin" and senha == "Root":
                    root.destroy()
                    abrir_menu_principal("DBA", "Administrador")
                else:
                    messagebox.showerror("Erro", "Usuário ou senha inválidos.")
        except mysql.connector.Error as e:
            messagebox.showerror("Erro de BD", str(e))

    # ----- Interface gráfica -----
    global root
    root = tk.Tk()
    root.title("Login - Sistema UniUFC-BD")
    root.geometry("350x200")
    root.resizable(False, False)

    tk.Label(root, text="Login:").pack(pady=(20, 0))
    entry_login = tk.Entry(root)
    entry_login.pack()

    tk.Label(root, text="Senha:").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()

    btn_login = tk.Button(root, text="Entrar", command=autenticar)
    btn_login.pack(pady=15)

    root.mainloop()
