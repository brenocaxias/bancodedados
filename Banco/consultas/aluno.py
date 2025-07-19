# consultas/consulta_aluno.py
import tkinter as tk
from tkinter import ttk, messagebox

def abrir_consulta_aluno(conexao):
    def consultar():
        matricula = entry_matricula.get()
        if not matricula:
            messagebox.showwarning("Atenção", "Informe a matrícula do aluno.")
            return

        try:
            cursor = conexao.cursor()

            # 1.1 Disciplinas matriculadas
            cursor.execute("""
                SELECT D.NOME FROM MATRICULAS M
                JOIN DISCIPLINAS D ON M.DISCIPLINA_ID = D.ID
                JOIN ALUNOS A ON A.ID = M.ALUNO_ID
                WHERE A.MATRICULA = %s AND M.NOTA_FINAL IS NULL
            """, (matricula,))
            result1 = cursor.fetchall()
            txt1 = "\n".join([r[0] for r in result1]) or "Nenhuma"

            # 1.2 Disciplinas concluídas
            cursor.execute("""
                SELECT D.NOME FROM MATRICULAS M
                JOIN DISCIPLINAS D ON M.DISCIPLINA_ID = D.ID
                JOIN ALUNOS A ON A.ID = M.ALUNO_ID
                WHERE A.MATRICULA = %s AND M.NOTA_FINAL IS NOT NULL
            """, (matricula,))
            result2 = cursor.fetchall()
            txt2 = "\n".join([r[0] for r in result2]) or "Nenhuma"

            # 1.3 Curso
            cursor.execute("""
                SELECT c.nome FROM alunos a
                JOIN cursos c ON a.curso_id = c.id
                WHERE a.matricula = %s
            """, (matricula,))
            curso = cursor.fetchone()
            txt3 = curso[0] if curso else "Desconhecido"

            # 1.4 Dados pessoais
            cursor.execute("""
                SELECT nome, endereco, tipo FROM alunos WHERE matricula = %s
            """, (matricula,))
            dados = cursor.fetchone()
            txt4 = f"Nome: {dados[0]}\nEndereço: {dados[1]}\nTipo: {dados[2]}" if dados else "Não encontrado"

            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Disciplinas Matriculadas:\n{txt1}\n\n")
            txt_resultado.insert(tk.END, f"📗 Disciplinas Concluídas:\n{txt2}\n\n")
            txt_resultado.insert(tk.END, f"📙 Curso do Aluno:\n{txt3}\n\n")
            txt_resultado.insert(tk.END, f"📕 Dados Pessoais:\n{txt4}")
            txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar:\n{e}")

    janela = tk.Toplevel()
    janela.title("Consulta - Aluno")
    janela.geometry("600x500")

    tk.Label(janela, text="Matrícula do Aluno:").pack(pady=5)
    entry_matricula = tk.Entry(janela, width=30)
    entry_matricula.pack()

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=25, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)
