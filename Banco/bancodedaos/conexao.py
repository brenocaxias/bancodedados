import mysql.connector

def conectar_bd(usuario,senha):
    try:
        conexao= mysql.connector.connect(
            host="localhost",
            user= usuario,
            password= senha,
            database="Equipe12345"#trocarpelo matricula do pedro henrique
        )
        return conexao
    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySql:",erro)
        return None