# crud/alunos_graduacao.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_crud_alunos_graduacao(conexao):
    def listar_alunos():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT a.id, a.matricula, a.nome, a.endereco, c.nome, ag.ano_ingresso
                FROM alunos a
                JOIN alunos_graduacao ag ON a.id = ag.aluno_id
                JOIN cursos c ON a.curso_id = c.id
                WHERE a.tipo = 'Graduacao'
            """)
            for id_, matricula, nome, endereco, curso, ano in cursor.fetchall():
                tree.insert("", "end", iid=id_, values=(matricula, nome, endereco, curso, ano))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos:\n{e}")

    def adicionar_aluno():
        matricula = simpledialog.askstring("Matrícula", "Digite a matrícula:")
        nome = simpledialog.askstring("Nome", "Digite o nome do aluno:")
        endereco = simpledialog.askstring("Endereço", "Digite o endereço:")
        curso_id = simpledialog.askinteger("ID do Curso", "Digite o ID do curso:")
        ano = simpledialog.askinteger("Ano de Ingresso", "Digite o ano de ingresso:")
        try:
            cursor = conexao.cursor()
            # Inserir na tabela alunos
            cursor.execute("""
                INSERT INTO alunos (matricula, nome, endereco, tipo, curso_id)
                VALUES (%s, %s, %s, 'Graduacao', %s)
            """, (matricula, nome, endereco, curso_id))
            aluno_id = cursor.lastrowid
            # Inserir na tabela alunos_graduacao
            cursor.execute("INSERT INTO alunos_graduacao (aluno_id, ano_ingresso) VALUES (%s, %s)", (aluno_id, ano))
            conexao.commit()
            listar_alunos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar aluno:\n{e}")

    def editar_ano():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        novo_ano = simpledialog.askinteger("Editar Ano", "Digite o novo ano de ingresso:")
        if novo_ano:
            try:
                cursor = conexao.cursor()
                cursor.execute("UPDATE alunos_graduacao SET ano_ingresso = %s WHERE aluno_id = %s", (novo_ano, item))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar ano:\n{e}")

    def excluir_aluno():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        if messagebox.askyesno("Confirmar", "Deseja excluir este aluno?"):
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM alunos_graduacao WHERE aluno_id = %s", (item,))
                cursor.execute("DELETE FROM alunos WHERE id = %s", (item,))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir aluno:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Alunos de Graduação")
    janela.geometry("800x400")

    tree = ttk.Treeview(janela, columns=("matricula", "nome", "endereco", "curso", "ano"), show="headings")
    for col in ("matricula", "nome", "endereco", "curso", "ano"):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True, pady=10)

    frame = tk.Frame(janela)
    frame.pack(pady=5)
    tk.Button(frame, text="Adicionar", width=15, command=adicionar_aluno).pack(side="left", padx=5)
    tk.Button(frame, text="Editar Ano", width=15, command=editar_ano).pack(side="left", padx=5)
    tk.Button(frame, text="Excluir", width=15, command=excluir_aluno).pack(side="left", padx=5)
    tk.Button(frame, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_alunos()
