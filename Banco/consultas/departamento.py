# consultas/consulta_departamento.py
import tkinter as tk
from tkinter import messagebox

def abrir_consulta_departamento(conexao):
    def consultar():
        depto_id = entry_id.get()
        if not depto_id:
            messagebox.showwarning("Atenção", "Informe o ID do departamento.")
            return

        try:
            cursor = conexao.cursor()

            # 2.1 Cursos do departamento
            cursor.execute("""
                SELECT NOME FROM CURSOS WHERE DEPARTAMENTO_ID = %s
            """, (depto_id,))
            cursos = [c[0] for c in cursor.fetchall()] or ["Nenhum"]

            # 2.2 Detalhes do departamento
            cursor.execute("""
                SELECT CODIGO, NOME FROM DEPARTAMENTOS WHERE ID = %s
            """, (depto_id,))
            depto = cursor.fetchone()
            detalhes = f"Código: {depto[0]}\nNome: {depto[1]}" if depto else "Não encontrado."

            txt_resultado.config(state="normal")
            txt_resultado.delete("1.0", tk.END)
            txt_resultado.insert(tk.END, f"📘 Detalhes do Departamento:\n{detalhes}\n\n")
            txt_resultado.insert(tk.END, f"📗 Cursos Associados:\n" + "\n".join(cursos))
            txt_resultado.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    janela = tk.Toplevel()
    janela.title("Consulta - Departamento")
    janela.geometry("600x400")

    tk.Label(janela, text="ID do Departamento:").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=10)

    txt_resultado = tk.Text(janela, wrap="word", height=20, state="disabled")
    txt_resultado.pack(padx=10, pady=10, fill="both", expand=True)
