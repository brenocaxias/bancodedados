# crud/disciplinas.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_crud_disciplinas(conexao):
    def listar_disciplinas():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT d.id, d.codigo, d.nome, d.ementa, d.creditos, d.tipo, c.nome 
                FROM disciplinas d
                LEFT JOIN cursos c ON d.curso_id = c.id
            """)
            for id_, codigo, nome, ementa, creditos, tipo, curso in cursor.fetchall():
                tree.insert("", "end", iid=id_, values=(codigo, nome, ementa[:40], creditos, tipo, curso or ""))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar disciplinas:\n{e}")

    def adicionar_disciplina():
        janela_add = tk.Toplevel()
        janela_add.title("Nova Disciplina")

        campos = {
            "Código": tk.Entry(janela_add),
            "Nome": tk.Entry(janela_add),
            "Ementa": tk.Text(janela_add, height=4, width=40),
            "Créditos": tk.Entry(janela_add),
            "Tipo (Obrigatória/Optativa)": tk.Entry(janela_add),
            "ID do Curso": tk.Entry(janela_add)
        }

        for i, (label, widget) in enumerate(campos.items()):
            tk.Label(janela_add, text=label + ":").grid(row=i, column=0, sticky="w")
            widget.grid(row=i, column=1, pady=2)

        def salvar():
            try:
                codigo = campos["Código"].get()
                nome = campos["Nome"].get()
                ementa = campos["Ementa"].get("1.0", "end").strip()
                creditos = int(campos["Créditos"].get())
                tipo = campos["Tipo (Obrigatória/Optativa)"].get()
                curso_id = int(campos["ID do Curso"].get())

                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO disciplinas (codigo, nome, ementa, creditos, tipo, curso_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (codigo, nome, ementa, creditos, tipo, curso_id))
                conexao.commit()
                janela_add.destroy()
                listar_disciplinas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar disciplina:\n{e}")

        tk.Button(janela_add, text="Salvar", command=salvar).grid(row=len(campos), columnspan=2, pady=10)

    def excluir_disciplina():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma disciplina para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir esta disciplina?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM disciplinas WHERE id = %s", (item,))
                conexao.commit()
                listar_disciplinas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir disciplina:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Disciplinas")
    janela.geometry("850x400")

    tree = ttk.Treeview(janela, columns=("codigo", "nome", "ementa", "creditos", "tipo", "curso"), show="headings")
    for col in ("codigo", "nome", "ementa", "creditos", "tipo", "curso"):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120 if col != "ementa" else 200)

    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_disciplina).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_disciplina).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_disciplinas()
