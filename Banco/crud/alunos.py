# crud/alunos.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

def abrir_crud_alunos(conexao):
    def listar_alunos():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, matricula, nome, endereco FROM alunos")
            for id_, matricula, nome, endereco in cursor.fetchall():
                tree.insert("", "end", iid=id_, values=(matricula, nome, endereco))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos:\n{e}")

    def adicionar_aluno():
        matricula = simpledialog.askstring("Nova Matrícula", "Digite a matrícula do aluno:")
        nome = simpledialog.askstring("Novo Nome", "Digite o nome do aluno:")
        endereco = simpledialog.askstring("Endereço", "Digite o endereço:")
        if matricula and nome:
            try:
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO alunos (matricula, nome, endereco) VALUES (%s, %s, %s)", (matricula, nome, endereco))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar aluno:\n{e}")

    def editar_aluno():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno para editar.")
            return
        values = tree.item(item, "values")
        novo_nome = simpledialog.askstring("Editar Nome", "Novo nome:", initialvalue=values[1])
        novo_endereco = simpledialog.askstring("Editar Endereço", "Novo endereço:", initialvalue=values[2])
        if novo_nome:
            try:
                cursor = conexao.cursor()
                cursor.execute("UPDATE alunos SET nome=%s, endereco=%s WHERE id=%s", (novo_nome, novo_endereco, item))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar aluno:\n{e}")

    def excluir_aluno():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar", "Deseja realmente excluir o aluno selecionado?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM alunos WHERE id=%s", (item,))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir aluno:\n{e}")

    # ----- Interface -----
    janela = tk.Toplevel()
    janela.title("CRUD - Alunos")
    janela.geometry("600x400")

    tree = ttk.Treeview(janela, columns=("matricula", "nome", "endereco"), show="headings")
    tree.heading("matricula", text="Matrícula")
    tree.heading("nome", text="Nome")
    tree.heading("endereco", text="Endereço")
    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_aluno).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Editar", width=15, command=editar_aluno).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_aluno).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_alunos()
