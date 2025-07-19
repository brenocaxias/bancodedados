# crud/alunos_posgraduacao.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_crud_alunos_posgraduacao(conexao):
    def listar_alunos():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT a.id, a.matricula, a.nome, a.endereco, c.nome, p.nome
                FROM alunos a
                JOIN alunos_posgraduacao ap ON a.id = ap.aluno_id
                JOIN professores p ON ap.orientador_id = p.id
                JOIN cursos c ON a.curso_id = c.id
                WHERE a.tipo = 'PosGraduacao'
            """)
            for id_, matricula, nome, endereco, curso, orientador in cursor.fetchall():
                tree.insert("", "end", iid=id_, values=(matricula, nome, endereco, curso, orientador))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar alunos:\n{e}")

    def adicionar_aluno():
        matricula = simpledialog.askstring("Matrícula", "Digite a matrícula:")
        nome = simpledialog.askstring("Nome", "Digite o nome do aluno:")
        endereco = simpledialog.askstring("Endereço", "Digite o endereço:")
        curso_id = simpledialog.askinteger("ID do Curso", "Digite o ID do curso de pós:")
        orientador_id = simpledialog.askinteger("ID do Orientador", "Digite o ID do professor orientador:")
        try:
            cursor = conexao.cursor()
            # alunos
            cursor.execute("""
                INSERT INTO alunos (matricula, nome, endereco, tipo, curso_id)
                VALUES (%s, %s, %s, 'PosGraduacao', %s)
            """, (matricula, nome, endereco, curso_id))
            aluno_id = cursor.lastrowid
            # alunos_posgraduacao
            cursor.execute("INSERT INTO alunos_posgraduacao (aluno_id, orientador_id) VALUES (%s, %s)",
                           (aluno_id, orientador_id))

            # formação básica
            while True:
                curso_formado = simpledialog.askstring("Curso de Formação", "Digite um curso formado (ou deixe vazio para parar):")
                if not curso_formado:
                    break
                cursor.execute("INSERT INTO formacao_aluno_pos (aluno_id, curso_formado) VALUES (%s, %s)",
                               (aluno_id, curso_formado))

            conexao.commit()
            listar_alunos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar aluno de pós:\n{e}")

    def ver_formacoes():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT curso_formado FROM formacao_aluno_pos WHERE aluno_id = %s", (item,))
            cursos = [row[0] for row in cursor.fetchall()]
            cursos_str = "\n".join(cursos) if cursos else "Nenhuma formação registrada."
            messagebox.showinfo("Formação Acadêmica", cursos_str)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar formação:\n{e}")

    def excluir_aluno():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        if messagebox.askyesno("Confirmar", "Deseja excluir este aluno de pós-graduação?"):
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM formacao_aluno_pos WHERE aluno_id = %s", (item,))
                cursor.execute("DELETE FROM alunos_posgraduacao WHERE aluno_id = %s", (item,))
                cursor.execute("DELETE FROM alunos WHERE id = %s", (item,))
                conexao.commit()
                listar_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir aluno:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Alunos de Pós-Graduação")
    janela.geometry("850x400")

    tree = ttk.Treeview(janela, columns=("matricula", "nome", "endereco", "curso", "orientador"), show="headings")
    for col in ("matricula", "nome", "endereco", "curso", "orientador"):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True, pady=10)

    frame = tk.Frame(janela)
    frame.pack(pady=5)
    tk.Button(frame, text="Adicionar", width=15, command=adicionar_aluno).pack(side="left", padx=5)
    tk.Button(frame, text="Ver Formação", width=15, command=ver_formacoes).pack(side="left", padx=5)
    tk.Button(frame, text="Excluir", width=15, command=excluir_aluno).pack(side="left", padx=5)
    tk.Button(frame, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_alunos()
