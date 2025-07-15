def disciplinas_atuais(conexao,matricula):
    cursor= conexao.cursor()
    query= """
        SELECT d.nome 
        FROM aluno_disciplina ad 
        JOIN disciplina d ON ad.cod_disciplina = d.codigo
        WHERE ad.matricula_aluno= %s and ad.status= 'Em andamento
        """
    cursor.execcute(query,(matricula,))
    resultados=cursor.fetchall()
    cursor.close()
    return resultados

def disciplinas_concluidas(conexao,matricula):
    cursor=conexao.cursor()
    query= """
        SELECT d.nome
        FROM aluno_disciplina ad
        JOIN disciplina d ON ad.cod_disciplina= d.consigo
        WHERE ad.matricula_aluno= %s and ad.status= 'Concluída'
        """
    cursor.execute(query,(matricula,))
    resultados= cursor.fetchall()
    cursor.close()
    return resultados

def curso_do_aluno(conexao,matricula):
    cursor= conexao.cursor()
    query= """
        SELECT c.nome
        FROM aluno a
        JOIN curso c ON a.cod_curso= c.codigo
        WHERE a.matricula= %s
        """
    cursor.execute(query,(matricula,))
    resultados=cursor.fetchall()
    cursor.close()
    return resultados

def dados_pessoais(conexao,matricula):
    cursor=conexao.cursor()
    query="""
        SELECT nome, endereco
        FROM aluno
        WHERE matricula= %s
        """
    cursor.execute(query,(matricula,))
    resultados= cursor.fetchall()
    cursor.close()
    return resultados