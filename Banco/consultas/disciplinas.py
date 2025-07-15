def alunos_da_disciplina(conexao,cod_disciplina):
    cursor=conexao.cursor()
    query="""
        SELECT a.matricula, a.nome
        FROM aluno_disciplina ad
        JOIN aluno a ON ad.matricula_aluno= a.matricula
        WHERE ad.cod_disciplina=%s
        """
    cursor.execute(query,(cod_disciplina,))
    resultados= cursor.fetchall()
    cursor.close()
    return resultados

def pre_requisitos(conexao,cod_disciplina):
    cursor= conexao.cursor()
    query="""
        SELECT d.codigo, d.nome
        FROM disciplina_pre_requisito pr
        JOIN disciplina d ON pr.cod_pre_requisito= d.codigo
        WHERE pr.cod_disciplina= %s
        """
    cursor.execute(query,(cod_disciplina,))
    resultados= cursor.fetchall()
    cursor.close()
    return resultados

def eh_pre_requist(conexao,cod_disciplina):
    cursor=conexao.cursor()
    query="""
        SELECT d.codigo, d.nome
        FROM disciplina_pre_requisito pr
        JOIN disciplina d ON pr.cod_disciplina= d.codigo
        WHERE pr.cod_pre_requisito=%s
        """
    cursor.execute(query,(cod_disciplina,))
    resultados= cursor.fetchall()
    cursor.close()
    return resultados