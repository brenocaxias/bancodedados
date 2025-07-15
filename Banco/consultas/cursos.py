def disciplinas_obrigatorias(conexao,cod_curso):
    cursor=conexao.cursor()
    query="""
        SELECT nome
        FROM disciplina
        WHERE cod_curso= %s AND tipo= 'Obrigatória'
        """
    cursor.execute(query,(cod_curso,))
    resultados=cursor.fetchall()
    cursor.close()
    return resultados

def disciplinas_optativas(conexao,cod_curso):
    cursor=conexao.cursor()
    query="""
        SELECT nome
        FROM disciplina
        WHERE cod_curso= %s AND tipo= 'Optativa'
        """
    cursor.execute(query,(cod_curso,))
    resultados=cursor.fetchall()
    cursor.close
    return resultados

def alunos_do_curso(conexao,cod_curso):
    cursor=conexao.cursor()
    query="""
        SELECT matricula,nome
        FROM aluno
        WHERE cod_curso=%s
        """
    cursor.execute(query,(cod_curso,))
    resultados= cursor.fetchall()
    cursor.close()
    return resultados

def alunos_concluintes_obrigatorias(conexao,cod_curso):
    cursor= conexao.cursor()
    query=""""
        SELECT a.matricula, a.nome
        FROM aluno a
        WHERE a.cod_aluno=%s AND NOT EXISTS(
            SELECT 1
            FROM disciplina d
            WHERE d.cod_curso= a.cod_curso AND d.tipo= 'Obrigatória'
            AND NOT EXISTS(
                SELECT 1 
                FROM aluno_disciplina ad
                WHERE ad.matricula_aluno= a.matricula
                AND ad.cod_disciplina= d.codigo 
                AND ad.status='Concluída'
            )
        )
        """
    cursor.execute(query,(cod_curso,))
    resultados=cursor.fetchall()
    cursor.close()
    return resultados

def alunos_sem_optativas(conexao, cod_curso):
    cursor=conexao.cursor()
    query="""
        SELECT a.matricula, a.nome
        FROM aluno a
        WHERE a.cod_aluno a= %s AND NOT EXISTS (
            SELECT 1
            FROM disciplina d
            JOIN aluno_disciplina ad ON d.codigo= ad.cod_disciplina
            WHERE d.tipo= 'Optativa'
            AND d.cod_curso= a.cod_curso
            AND ad.matricula_aluno= a.matricula
        )
        """
    cursor.execute(query,(cod_curso,))
    resultados= cursor.fetchall()
    cursor.close()
    return resultados