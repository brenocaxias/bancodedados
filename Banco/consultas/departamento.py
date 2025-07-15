def cursos_do_departamento(conexao,cod_departamento):
    cursor= conexao.cursor()
    query="""
        SELECT c.codigo, c.nome
        FROM curso c
        WHERE c.cod_departamento=%s
        """
    cursor.execute(query,(cod_departamento,))
    resultados= cursor.fetchall()
    cursor.close()
    return resultados

def dados_departamento(conexao,cod_departamento):
    cursor=conexao.cursor()
    query="""
        SELECT codigo, nome
        FROM departamento
        WHERE codigo= %s
        """
    cursor.execute(query,(cod_departamento,))
    resultados=cursor.fetchall()
    cursor.close()
    return resultados
