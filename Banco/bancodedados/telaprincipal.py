# menu_principal.py
import tkinter as tk
from tkinter import messagebox
from crud.alunos import abrir_crud_alunos
from crud.professores import abrir_crud_professores
from crud.disciplinas import abrir_crud_disciplinas
from crud.cursos import abrir_crud_cursos
from crud.departamentos import abrir_crud_departamentos
from crud.usuarios import abrir_crud_usuarios
from crud.alunos_graduacao import abrir_crud_alunos_graduacao
from crud.alunos_posgraduacao import abrir_crud_alunos_posgraduacao
from crud.matriculas import abrir_matriculas
from consultas.aluno import abrir_consulta_aluno
from crud.contatos import abrir_gerenciador_contatos
from consultas.disciplinas import abrir_consulta_disciplina
from consultas.orientador import abrir_consulta_orientador
from consultas.departamento import abrir_consulta_departamento

def menu_principal(tipo_usuario, nome_usuario, conexao):
    tipo_usuario = tipo_usuario.strip().lower()
    root = tk.Tk()
    root.title(f"UniUFC-BD - Menu Principal ({tipo_usuario})")
    root.geometry("500x400")

    tk.Label(root, text=f"Bem-vindo(a), {nome_usuario}!", font=("Arial", 14)).pack(pady=20)

    # DBA: acesso total
    if tipo_usuario == "dba":
        tk.Button(root, text="Gerenciar Alunos", width=30, command=lambda:abrir_crud_alunos(conexao)).pack(pady=5)
        tk.Button(root, text="Gerenciar Professores", width=30, command=lambda:abrir_crud_professores(conexao)).pack(pady=5)
        tk.Button(root, text="Gerenciar Disciplinas", width=30, command=lambda:abrir_crud_disciplinas(conexao)).pack(pady=5)
        tk.Button(root, text="Gerenciar Cursos", width=30, command=lambda: abrir_crud_cursos(conexao)).pack(pady=5)
        tk.Button(root, text="Gerenciar Departamentos", width=30, command=lambda:abrir_crud_departamentos(conexao)).pack(pady=5)
        tk.Button(root, text="Consultas SQL", width=30, command=lambda: messagebox.showinfo("Ação", "Abrir Módulo de Consultas")).pack(pady=5)
        tk.Button(root, text="Gerenciar Usuários", width=30, command=lambda: abrir_crud_usuarios(conexao)).pack(pady=5)
        tk.Button(root, text="Alunos de Graduação", width=30, command=lambda: abrir_crud_alunos_graduacao(conexao)).pack(pady=5)
        tk.Button(root, text="Alunos de Pós-Graduação", width=30, command=lambda: abrir_crud_alunos_posgraduacao(conexao)).pack(pady=5)
        tk.Button(root, text="Matrícula de Aluno", width=30, command=lambda: abrir_matriculas(conexao)).pack(pady=5)
        tk.Button(root, text="Consultar Dados do Aluno", width=30, command=lambda: abrir_consulta_aluno(conexao)).pack(pady=5)
        tk.Button(root, text="Gerenciar Contatos", width=30, command=lambda: abrir_gerenciador_contatos(conexao)).pack(pady=5)
        tk.Button(root, text="Consultar Disciplina", command=lambda: abrir_consulta_disciplina(conexao)).pack(pady=5)
        tk.Button(root, text="Consultar Orientador", command=lambda: abrir_consulta_orientador(conexao)).pack(pady=5)
        tk.Button(root, text="Consultar Departamento", command=lambda: abrir_consulta_departamento(conexao)).pack(pady=5)
    # Funcionário: acesso restrito ao departamento
    elif tipo_usuario == "servidor":
        tk.Button(root, text="Consultar Departamento", command=lambda: abrir_consulta_departamento(conexao)).pack(pady=5)
        tk.Button(root, text="Visualizar Cursos e Disciplinas", width=30, command=lambda: messagebox.showinfo("Ação", "Listar cursos e disciplinas")).pack(pady=5)

    # Professor: acesso somente à leitura de suas disciplinas/notas
    elif tipo_usuario == "professor":
        tk.Button(root, text="Minhas Disciplinas", width=30, command=lambda: messagebox.showinfo("Ação", "Listar disciplinas que você ministra")).pack(pady=5)
        tk.Button(root, text="Alunos e Notas", width=30, command=lambda: messagebox.showinfo("Ação", "Ver alunos/notas da disciplina")).pack(pady=5)
        tk.Button(root, text="Consultar Dados do Aluno", width=30, command=lambda: abrir_consulta_aluno(conexao)).pack(pady=5)
        tk.Button(root, text="Consultar Disciplina", command=lambda: abrir_consulta_disciplina(conexao)).pack(pady=5)
        tk.Button(root, text="Consultar Orientador", command=lambda: abrir_consulta_orientador(conexao)).pack(pady=5)
    # Aluno: acesso apenas às suas informações
    elif tipo_usuario == "aluno":
        tk.Button(root, text="Minhas Disciplinas", width=30, command=lambda: messagebox.showinfo("Ação", "Ver disciplinas matriculadas")).pack(pady=5)
        tk.Button(root, text="Histórico Escolar", width=30, command=lambda: messagebox.showinfo("Ação", "Ver disciplinas concluídas")).pack(pady=5)
        tk.Button(root, text="Dados Pessoais", width=30, command=lambda: messagebox.showinfo("Ação", "Ver seus dados")).pack(pady=5)
        tk.Button(root, text="Consultar Dados do Aluno", width=30, command=lambda: abrir_consulta_aluno(conexao)).pack(pady=5)
    tk.Button(root, text="sair", width=30, command=root.destroy).pack(pady=20)

    root.mainloop()
