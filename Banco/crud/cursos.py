# crud/cursos.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_crud_cursos(conexao):
    def listar_cursos():
        for row in tree.get_children():
            tree.delete(row)
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT c.id, c.codigo, c.nome, c.creditos_minimos, d.nome 
                FROM cursos c
                LEFT JOIN departamentos d ON c.departamento_id = d.id
            """)
            for id_, codigo, nome, creditos, departamento in cursor.fetchall():
                tree.insert("", "end", iid=id_, values=(codigo, nome, creditos, departamento or ""))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar cursos:\n{e}")

    def adicionar_curso():
        janela_add = tk.Toplevel()
        janela_add.title("Novo Curso")

        campos = {
            "Código": tk.Entry(janela_add),
            "Nome": tk.Entry(janela_add),
            "Créditos Mínimos": tk.Entry(janela_add),
            "ID do Departamento": tk.Entry(janela_add)
        }

        for i, (label, widget) in enumerate(campos.items()):
            tk.Label(janela_add, text=label + ":").grid(row=i, column=0, sticky="w")
            widget.grid(row=i, column=1, pady=2)

        def salvar():
            try:
                codigo = campos["Código"].get()
                nome = campos["Nome"].get()
                creditos = int(campos["Créditos Mínimos"].get())
                depto_id = int(campos["ID do Departamento"].get())

                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO cursos (codigo, nome, creditos_minimos, departamento_id)
                    VALUES (%s, %s, %s, %s)
                """, (codigo, nome, creditos, depto_id))
                conexao.commit()
                janela_add.destroy()
                listar_cursos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar curso:\n{e}")

        tk.Button(janela_add, text="Salvar", command=salvar).grid(row=len(campos), columnspan=2, pady=10)

    def excluir_curso():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um curso para excluir.")
            return
        confirmar = messagebox.askyesno("Confirmar", "Deseja excluir este curso?")
        if confirmar:
            try:
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM cursos WHERE id = %s", (item,))
                conexao.commit()
                listar_cursos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir curso:\n{e}")

    janela = tk.Toplevel()
    janela.title("CRUD - Cursos")
    janela.geometry("700x400")

    tree = ttk.Treeview(janela, columns=("codigo", "nome", "creditos", "departamento"), show="headings")
    for col in ("codigo", "nome", "creditos", "departamento"):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True, pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="Adicionar", width=15, command=adicionar_curso).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Excluir", width=15, command=excluir_curso).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="Fechar", width=15, command=janela.destroy).pack(side="left", padx=5)

    listar_cursos()
