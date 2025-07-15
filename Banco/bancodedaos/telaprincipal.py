# menu_principal.py
import tkinter as tk
from tkinter import messagebox
from crud.alunos import abrir_crud_alunos
from crud.professores import abrir_crud_professores
from crud.disciplinas import abrir_crud_disciplinas
def menu_principal(tipo_usuario, nome_usuario, conexao):
    root = tk.Tk()
    root.title(f"UniUFC-BD - Menu Principal ({tipo_usuario})")
    root.geometry("500x400")

    tk.Label(root, text=f"Bem-vindo(a), {nome_usuario}!", font=("Arial", 14)).pack(pady=20)

    # DBA: acesso total
    if tipo_usuario == "DBA":
        tk.Button(root, text="Gerenciar Alunos", width=30, command=lambda:abrir_crud_alunos(conexao).pack(pady=5))
        tk.Button(root, text="Gerenciar Professores", width=30, command=lambda:abrir_crud_professores(conexao).pack(pady=5))
        tk.Button(root, text="Gerenciar Disciplinas", width=30, command=lambda:abrir_crud_disciplinas(conexao).pack(pady=5))
        tk.Button(root, text="Gerenciar Cursos", width=30, command=lambda: messagebox.showinfo("Ação", "Abrir CRUD Cursos")).pack(pady=5)
        tk.Button(root, text="Gerenciar Departamentos", width=30, command=lambda: messagebox.showinfo("Ação", "Abrir CRUD Departamentos")).pack(pady=5)
        tk.Button(root, text="Consultas SQL", width=30, command=lambda: messagebox.showinfo("Ação", "Abrir Módulo de Consultas")).pack(pady=5)

    # Funcionário: acesso restrito ao departamento
    elif tipo_usuario == "Servidor":
        tk.Button(root, text="Consultar Departamento", width=30, command=lambda: messagebox.showinfo("Ação", "Consultar dados do seu departamento")).pack(pady=5)
        tk.Button(root, text="Visualizar Cursos e Disciplinas", width=30, command=lambda: messagebox.showinfo("Ação", "Listar cursos e disciplinas")).pack(pady=5)

    # Professor: acesso somente à leitura de suas disciplinas/notas
    elif tipo_usuario == "Professor":
        tk.Button(root, text="Minhas Disciplinas", width=30, command=lambda: messagebox.showinfo("Ação", "Listar disciplinas que você ministra")).pack(pady=5)
        tk.Button(root, text="Alunos e Notas", width=30, command=lambda: messagebox.showinfo("Ação", "Ver alunos/notas da disciplina")).pack(pady=5)

    # Aluno: acesso apenas às suas informações
    elif tipo_usuario == "Aluno":
        tk.Button(root, text="Minhas Disciplinas", width=30, command=lambda: messagebox.showinfo("Ação", "Ver disciplinas matriculadas")).pack(pady=5)
        tk.Button(root, text="Histórico Escolar", width=30, command=lambda: messagebox.showinfo("Ação", "Ver disciplinas concluídas")).pack(pady=5)
        tk.Button(root, text="Dados Pessoais", width=30, command=lambda: messagebox.showinfo("Ação", "Ver seus dados")).pack(pady=5)

    tk.Button(root, text="Sair", width=30, command=root.destroy).pack(pady=20)

    root.mainloop()
