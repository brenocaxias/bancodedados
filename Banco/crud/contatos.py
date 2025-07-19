# crud/contatos.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def abrir_gerenciador_contatos(conexao):
    def listar():
        tipo = tipo_var.get()
        id_pessoa = entry_id.get()
        if not id_pessoa:
            messagebox.showwarning("Atenção", "Informe o ID da pessoa.")
            return

        for i in tree_email.get_children():
            tree_email.delete(i)
        for i in tree_fone.get_children():
            tree_fone.delete(i)

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, email FROM emails
                WHERE pessoa_tipo = %s AND pessoa_id = %s
            """, (tipo, id_pessoa))
            for id_, email in cursor.fetchall():
                tree_email.insert("", "end", iid=f"e{id_}", values=(email,))

            cursor.execute("""
                SELECT id, numero, descricao FROM telefones
                WHERE pessoa_tipo = %s AND pessoa_id = %s
            """, (tipo, id_pessoa))
            for id_, numero, desc in cursor.fetchall():
                tree_fone.insert("", "end", iid=f"t{id_}", values=(numero, desc))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar contatos:\n{e}")

    def adicionar_email():
        tipo = tipo_var.get()
        id_pessoa = entry_id.get()
        email = simpledialog.askstring("Novo E-mail", "Digite o e-mail:")
        if email:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO emails (email, pessoa_tipo, pessoa_id)
                    VALUES (%s, %s, %s)
                """, (email, tipo, id_pessoa))
                conexao.commit()
                listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar e-mail:\n{e}")

    def adicionar_telefone():
        tipo = tipo_var.get()
        id_pessoa = entry_id.get()
        numero = simpledialog.askstring("Número", "Digite o telefone:")
        desc = simpledialog.askstring("Descrição", "Digite a descrição (Ex: Celular, WhatsApp):")
        if numero and desc:
            try:
                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO telefones (numero, descricao, pessoa_tipo, pessoa_id)
                    VALUES (%s, %s, %s, %s)
                """, (numero, desc, tipo, id_pessoa))
                conexao.commit()
                listar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar telefone:\n{e}")

    def excluir_email():
        item = tree_email.focus()
        if not item:
            return
        id_ = item[1:]  # remove 'e'
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM emails WHERE id = %s", (id_,))
            conexao.commit()
            listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir e-mail:\n{e}")

    def excluir_telefone():
        item = tree_fone.focus()
        if not item:
            return
        id_ = item[1:]  # remove 't'
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM telefones WHERE id = %s", (id_,))
            conexao.commit()
            listar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir telefone:\n{e}")

    # Janela
    janela = tk.Toplevel()
    janela.title("Contatos: Telefones e E-mails")
    janela.geometry("700x500")

    tk.Label(janela, text="Tipo de Pessoa:").pack()
    tipo_var = tk.StringVar(value="Aluno")
    tipo_menu = ttk.Combobox(janela, textvariable=tipo_var, values=["Aluno", "Professor"], state="readonly")
    tipo_menu.pack()

    tk.Label(janela, text="ID da Pessoa:").pack(pady=5)
    entry_id = tk.Entry(janela)
    entry_id.pack()

    tk.Button(janela, text="Buscar Contatos", command=listar).pack(pady=5)

    tk.Label(janela, text="E-mails").pack()
    tree_email = ttk.Treeview(janela, columns=("email",), show="headings")
    tree_email.heading("email", text="E-mail")
    tree_email.pack(pady=5, fill="x")

    frame_email = tk.Frame(janela)
    frame_email.pack(pady=2)
    tk.Button(frame_email, text="Adicionar E-mail", command=adicionar_email).pack(side="left", padx=5)
    tk.Button(frame_email, text="Excluir E-mail", command=excluir_email).pack(side="left", padx=5)

    tk.Label(janela, text="Telefones").pack(pady=5)
    tree_fone = ttk.Treeview(janela, columns=("numero", "descricao"), show="headings")
    tree_fone.heading("numero", text="Número")
    tree_fone.heading("descricao", text="Descrição")
    tree_fone.pack(pady=5, fill="x")

    frame_fone = tk.Frame(janela)
    frame_fone.pack(pady=2)
    tk.Button(frame_fone, text="Adicionar Telefone", command=adicionar_telefone).pack(side="left", padx=5)
    tk.Button(frame_fone, text="Excluir Telefone", command=excluir_telefone).pack(side="left", padx=5)
