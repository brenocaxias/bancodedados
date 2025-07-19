# consultas/consulta_orientador.py
import tkinter as tk
from tkinter import messagebox

def abrir_consulta_orientador(conexao):
    def consultar():
        prof_id = entry_id.get()
        if not prof_id:
            messagebox.showwarning("Atenção", "Informe o ID do professor orientador.")
            return

        try:
            cursor = conexao.cursor()

            # 5.1 Alunos orientandos
            cursor.execute("""
                SELECT a.nome FROM alunos_posgraduacao ap
                JOIN alunos a ON ap.aluno_id = a.id
                WHERE ap.orientador_id = %s
            """, (prof_id,))
            orientandos = [r[0] for r in cursor.fetchall()] or ["Nenhum"]

            # 5.2 Disciplinas ministradas
            cursor.execute("""
                SELECT nome, creditos FROM disciplinas
                WHERE id IN (
                    SELECT disciplina_id FROM disciplinas_professores WHERE professor_id = %s
                )
            """, (prof_id,))
            disciplinas = cursor.fetchall()
            lista_disciplinas = [f"{nome} ({creditos} créditos)" for nome, creditos in disciplinas] or ["Nenhuma"]

            # 5.3 Total de créditos
            total_creditos = sum([int(creditos) for _, creditos in disciplinas]) if disciplinas else 0

            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Alunos Orientandos (Pós):\n" + "\n".join(orientandos) + "\n\n")
            txt_resultado.insert(tk.END, f"📗 Disciplinas Ministradas:\n" + "\n".join(lista_disciplinas) + "\n\n")
            txt_resultado.insert(tk.END, f"📙 Total de Créditos Ministrados: {total_creditos}")
            txt_resultado.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    janela = tk.Toplevel()
    janela.title("Consulta - Orientador")
    janela.geometry("650x500")

    tk.Label(janela, text="ID do Professor (Orientador):").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=25, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)
