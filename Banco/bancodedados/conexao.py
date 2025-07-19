import mysql.connector
from mysql.connector import Error

def conectar_bd(usuario,senha, host='localhost',database='Equipe521461'):
    try:
        conexao= mysql.connector.connect(
            host="localhost",
            user= usuario,
            password= senha,
            database="Equipe521461"
        )
        if conexao.is_connected():
            return conexao
    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySql:",erro)
        return None 