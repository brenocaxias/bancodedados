# crud/matriculas.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_matriculas(conexao):
    def listar_matriculas():
        for row in tree.get_children():
            tree.delete(row)
        aluno_id = entry_aluno_id.get()
        if not aluno_id:
            messagebox.showwarning("Atenção", "Digite o ID do aluno.")
            return
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT d.nome, m.nota_final, m.frequencia
                FROM matriculas m
                JOIN disciplinas d ON m.disciplina_id = d.id
                WHERE m.aluno_id = %s
            """, (aluno_id,))
            for nome, nota, freq in cursor.fetchall():
                tree.insert("", "end", values=(nome, nota, f"{freq}%"))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar matrículas:\n{e}")

    def adicionar_matricula():
        aluno_id = entry_aluno_id.get()
        if not aluno_id:
            messagebox.showwarning("Atenção", "Digite o ID do aluno.")
            return
        disciplina_id = simpledialog.askinteger("ID da Disciplina", "Digite o ID da disciplina:")
        nota = simpledialog.askfloat("Nota Final", "Digite a nota (ex: 8.5):")
        freq = simpledialog.askfloat("Frequência (%)", "Digite a frequência (ex: 90):")
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO matriculas (aluno_id, disciplina_id, nota_final, frequencia)
                VALUES (%s, %s, %s, %s)
            """, (aluno_id, disciplina_id, nota, freq))
            conexao.commit()
            listar_matriculas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar matrícula:\n{e}")

    def editar_matricula():
        aluno_id = entry_aluno_id.get()
        if not aluno_id:
            messagebox.showwarning("Atenção", "Digite o ID do aluno.")
            return
        disciplina_id = simpledialog.askinteger("ID da Disciplina", "Digite o ID da disciplina a editar:")
        nova_nota = simpledialog.askfloat("Nova Nota", "Digite a nova nota:")
        nova_freq = simpledialog.askfloat("Nova Frequência", "Digite a nova frequência:")
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE matriculas
                SET nota_final = %s, frequencia = %s
                WHERE aluno_id = %s AND disciplina_id = %s
            """, (nova_nota, nova_freq, aluno_id, disciplina_id))
            conexao.commit()
            listar_matriculas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar matrícula:\n{e}")

    def excluir_matricula():
        aluno_id = entry_aluno_id.get()
        if not aluno_id:
            messagebox.showwarning("Atenção", "Digite o ID do aluno.")
            return
        disciplina_id = simpledialog.askinteger("ID da Disciplina", "Digite o ID da disciplina a remover:")
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir esta matrícula?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM matriculas WHERE aluno_id = %s AND disciplina_id = %s", (aluno_id, disciplina_id))
                conexao.commit()
                listar_matriculas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir matrícula:\n{e}")

    # --- Interface ---
    janela = tk.Toplevel()
    janela.title("Matrículas de Aluno em Disciplinas")
    janela.geometry("700x400")

    tk.Label(janela, text="ID do Aluno:").pack(pady=(10, 0))
    entry_aluno_id = tk.Entry(janela)
    entry_aluno_id.pack()

    tk.Button(janela, text="Listar Matrículas", command=listar_matriculas).pack(pady=5)

    tree = ttk.Treeview(janela, columns=("disciplina", "nota", "frequencia"), show="headings")
    tree.heading("disciplina", text="Disciplina")
    tree.heading("nota", text="Nota Final")
    tree.heading("frequencia", text="Frequência")
    tree.pack(fill="both", expand=True, pady=10)

    frame = tk.Frame(janela)
    frame.pack(pady=5)
    tk.Button(frame, text="Adicionar", width=15, command=adicionar_matricula).pack(side="left", padx=5)
    tk.Button(frame, text="Editar", width=15, command=editar_matricula).pack(side="left", padx=5)
    tk.Button(frame, text="Excluir", width=15, command=excluir_matricula).pack(side="left", padx=5)
    tk.Button(frame, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)
