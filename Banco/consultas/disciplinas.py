# consultas/consulta_disciplina.py
import tkinter as tk
from tkinter import messagebox

def abrir_consulta_disciplina(conexao):
    def consultar():
        disc_id = entry_id.get()
        if not disc_id:
            messagebox.showwarning("Atenção", "Informe o ID da disciplina.")
            return

        try:
            cursor = conexao.cursor()

            # 4.1 Alunos matriculados
            cursor.execute("""
                SELECT A.NOME FROM MATRICULAS M
                JOIN ALUNOS A ON M.ALUNO_ID = A.ID
                WHERE M.DISCIPLINA_ID = %s
            """, (disc_id,))
            alunos = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # 4.2 Pré-requisitos da disciplina
            cursor.execute("""
                SELECT D2.NOME FROM PRE_REQUISITOS PR
                JOIN DISCIPLINAS D1 ON PR.DISCIPLINA_ID = D1.ID
                JOIN DISCIPLINAS D2 ON PR.PREREQUISITO_ID = D2.ID
                WHERE D1.ID = %s
            """, (disc_id,))
            prereqs = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # 4.3 Disciplinas que têm esta como pré-requisito
            cursor.execute("""
                SELECT D1.NOME FROM PRE_REQUISITOS PR
                JOIN DISCIPLINAS D1 ON PR.DISCIPLINA_ID = D1.ID
                WHERE PR.PREREQUISITO_ID = %s
            """, (disc_id,))
            dependentes = [r[0] for r in cursor.fetchall()] or ["Nenhuma"]

            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Alunos Matriculados:\n" + "\n".join(alunos) + "\n\n")
            txt_resultado.insert(tk.END, f"📗 Pré-requisitos desta disciplina:\n" + "\n".join(prereqs) + "\n\n")
            txt_resultado.insert(tk.END, f"📙 Disciplinas que dependem desta:\n" + "\n".join(dependentes))
            txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    janela = tk.Toplevel()
    janela.title("Consulta - Disciplina")
    janela.geometry("650x500")

    tk.Label(janela, text="ID da Disciplina:").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=25, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)
