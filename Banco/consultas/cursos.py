# consultas/consulta_curso.py
import tkinter as tk
from tkinter import messagebox

def abrir_consulta_curso(conexao):
    def consultar():
        curso_id = entry_id.get()
        if not curso_id:
            messagebox.showwarning("Atenção", "Informe o ID do curso.")
            return

        try:
            cursor = conexao.cursor()

            # 3.1 Disciplinas obrigatórias
            cursor.execute("SELECT nome FROM disciplinas WHERE tipo = 'Obrigatória' AND curso_id = %s", (curso_id,))
            obrigatorias = [r[0] for r in cursor.fetchall()] or ["Nenhuma"]

            # 3.2 Disciplinas optativas
            cursor.execute("SELECT nome FROM disciplinas WHERE tipo = 'Optativa' AND curso_id = %s", (curso_id,))
            optativas = [r[0] for r in cursor.fetchall()] or ["Nenhuma"]

            # 3.3 Alunos do curso
            cursor.execute("SELECT nome FROM alunos WHERE curso_id = %s", (curso_id,))
            alunos = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # 3.4 Alunos que fizeram todas as obrigatórias
            cursor.execute("""
                SELECT DISTINCT a.nome
                FROM alunos a
                WHERE a.curso_id = %s AND NOT EXISTS (
                    SELECT d.id FROM disciplinas d
                    WHERE d.tipo = 'Obrigatória' AND d.curso_id = %s
                    EXCEPT
                    SELECT m.disciplina_id FROM matriculas m WHERE m.aluno_id = a.id AND m.nota_final IS NOT NULL
                )
            """, (curso_id, curso_id))
            completos = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # 3.5 Alunos que não fizeram nenhuma optativa
            cursor.execute("""
                SELECT a.nome
                FROM alunos a
                WHERE a.curso_id = %s AND NOT EXISTS (
                    SELECT 1 FROM matriculas m
                    JOIN disciplinas d ON m.disciplina_id = d.id
                    WHERE m.aluno_id = a.id AND d.tipo = 'Optativa' AND d.curso_id = %s
                )
            """, (curso_id, curso_id))
            nenhum_optativa = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Disciplinas Obrigatórias:\n" + "\n".join(obrigatorias) + "\n\n")
            txt_resultado.insert(tk.END, f"📗 Disciplinas Optativas:\n" + "\n".join(optativas) + "\n\n")
            txt_resultado.insert(tk.END, f"📙 Alunos Matriculados:\n" + "\n".join(alunos) + "\n\n")
            txt_resultado.insert(tk.END, f"📕 Alunos que concluíram TODAS obrigatórias:\n" + "\n".join(completos) + "\n\n")
            txt_resultado.insert(tk.END, f"📕 Alunos que NÃO fizeram nenhuma optativa:\n" + "\n".join(nenhum_optativa))
            txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    janela = tk.Toplevel()
    janela.title("Consulta - Curso")
    janela.geometry("700x500")

    tk.Label(janela, text="ID do Curso:").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=25, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)
