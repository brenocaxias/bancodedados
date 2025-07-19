-- 1.1 Dado o número (matrícula) do aluno, deseja-se saber em quais disciplinas está atualmente matriculado:
USE Equipe521461;
SELECT
    A.nome AS Nome_Aluno,
    D.nome AS Nome_Disciplina,
    AD.media_final AS Media_Final,
    AD.frequencia AS Frequencia
FROM
    ALUNO AS A
JOIN
    ALUNO_DISCIPLINA AS AD ON A.matricula = AD.matricula_aluno
JOIN
    DISCIPLINA AS D ON AD.codigo_disciplina = D.codigo
WHERE
    A.matricula = 20230001; -- Substitua pela matrícula do aluno desejado
    
    
-- 1.2 Dado o número (matrícula) do aluno, deseja-se saber quais disciplinas já concluiu:
USE Equipe521461;
SELECT
    A.nome AS Nome_Aluno,
    D.nome AS Nome_Disciplina,
    AD.media_final AS Media_Final,
    AD.frequencia AS Frequencia
FROM
    ALUNO AS A
JOIN
    ALUNO_DISCIPLINA AS AD ON A.matricula = AD.matricula_aluno
JOIN
    DISCIPLINA AS D ON AD.codigo_disciplina = D.codigo
WHERE
    A.matricula = 20230001 -- Substitua pela matrícula do aluno desejado
    AND AD.media_final >= 7.0;
    

-- 1.3 Dado o número (matrícula) do aluno, deseja-se saber qual o curso deste aluno:
USE Equipe521461;
SELECT
    A.nome AS Nome_Aluno,
    C.nome AS Nome_Curso,
    C.codigo AS Codigo_Curso
FROM
    ALUNO AS A
JOIN
    CURSO AS C ON A.codigo_curso = C.codigo
WHERE
    A.matricula = 20230001; -- Substitua pela matrícula do aluno desejado
    
    
-- 1.4 Dado o número (matrícula) do aluno, deseja-se saber os dados pessoais sobre o aluno:
USE Equipe521461;
SELECT
    A.matricula,
    A.nome,
    A.endereco,
    A.tipo_aluno,
    C.nome AS Nome_Curso -- Inclui o nome do curso para contexto
FROM
    ALUNO AS A
JOIN
    CURSO AS C ON A.codigo_curso = C.codigo
WHERE
    A.matricula = 20230001; -- Substitua pela matrícula do aluno desejado
    

-- 2.1 Dado o código de um departamento, deseja-se saber quais cursos estão sob a responsabilidade do departamento:
USE Equipe521461;
SELECT
    D.nome AS Nome_Departamento,
    C.nome AS Nome_Curso,
    C.codigo AS Codigo_Curso,
    C.quantidade_minima_creditos AS Creditos_Minimos
FROM
    DEPARTAMENTO AS D
JOIN
    CURSO AS C ON D.codigo = C.codigo_departamento
WHERE
    D.codigo = 100; -- Substitua pelo código do departamento desejado
    
    
-- 2.2 Dado o código de um departamento, deseja-se saber detalhes sobre o departamento:
USE Equipe521461;
SELECT
    codigo AS Codigo_Departamento,
    nome AS Nome_Departamento
FROM
    DEPARTAMENTO
WHERE
    codigo = 100; -- Substitua pelo código do departamento desejado
    
    
-- 3.1 Dado um curso, deseja-se saber quais são as disciplinas obrigatórias do curso:
USE Equipe521461;
SELECT
    C.nome AS Nome_Curso,
    D.nome AS Nome_Disciplina,
    D.numero_creditos AS Creditos,
    D.tipo
FROM
    CURSO AS C
JOIN
    DISCIPLINA AS D ON C.codigo = D.codigo_curso
WHERE
    C.codigo = 10 -- Substitua pelo código do curso desejado
    AND D.tipo = 'obrigatoria';
    
    
-- 3.2 Dado um curso, deseja-se saber quais são as disciplinas optativas do curso:
USE Equipe521461;
SELECT
    C.nome AS Nome_Curso,
    D.nome AS Nome_Disciplina,
    D.numero_creditos AS Creditos,
    D.tipo
FROM
    CURSO AS C
JOIN
    DISCIPLINA AS D ON C.codigo = D.codigo_curso
WHERE
    C.codigo = 10 -- Substitua pelo código do curso desejado
    AND D.tipo = 'optativa';
    
    
-- 3.3 Dado um curso, deseja-se saber quais são os alunos desse curso:
USE Equipe521461;
SELECT
    C.nome AS Nome_Curso,
    A.matricula,
    A.nome AS Nome_Aluno,
    A.tipo_aluno
FROM
    CURSO AS C
JOIN
    ALUNO AS A ON C.codigo = A.codigo_curso
WHERE
    C.codigo = 10; -- Substitua pelo código do curso desejado
    
    
-- 3.4 Dado um curso, deseja-se saber quais alunos deste já fizeram todas as disciplinas obrigatórias:
USE Equipe521461;
SELECT
    A.matricula,
    A.nome AS Nome_Aluno,
    C.nome AS Nome_Curso
FROM
    ALUNO AS A
JOIN
    CURSO AS C ON A.codigo_curso = C.codigo
WHERE
    C.codigo = 10 -- Substitua pelo código do curso desejado
    AND A.tipo_aluno = 'graduacao' -- Assumindo que apenas alunos de graduação têm "todas as obrigatórias"
    AND (
        SELECT COUNT(DISTINCT D.codigo)
        FROM DISCIPLINA AS D
        WHERE D.codigo_curso = C.codigo AND D.tipo = 'obrigatoria'
    ) = (
        SELECT COUNT(DISTINCT AD.codigo_disciplina)
        FROM ALUNO_DISCIPLINA AS AD
        JOIN DISCIPLINA AS D2 ON AD.codigo_disciplina = D2.codigo
        WHERE AD.matricula_aluno = A.matricula
        AND D2.codigo_curso = C.codigo
        AND D2.tipo = 'obrigatoria'
        AND AD.media_final >= 7.0 -- Critério de conclusão
    );


-- 3.5 Dado um curso, deseja-se saber quais alunos não fizeram nenhuma disciplina optativa:
USE Equipe521461;
SELECT
    A.matricula,
    A.nome AS Nome_Aluno,
    C.nome AS Nome_Curso
FROM
    ALUNO AS A
JOIN
    CURSO AS C ON A.codigo_curso = C.codigo
WHERE
    C.codigo = 10 -- Substitua pelo código do curso desejado
    AND A.matricula NOT IN (
        SELECT AD.matricula_aluno
        FROM ALUNO_DISCIPLINA AS AD
        JOIN DISCIPLINA AS D ON AD.codigo_disciplina = D.codigo
        WHERE D.codigo_curso = C.codigo AND D.tipo = 'optativa'
    );
    
    
-- 4.1 Dado uma disciplina, deseja-se saber quais alunos foram matriculados na disciplina:
USE Equipe521461;
SELECT
    D.nome AS Nome_Disciplina,
    A.matricula,
    A.nome AS Nome_Aluno,
    AD.media_final,
    AD.frequencia
FROM
    DISCIPLINA AS D
JOIN
    ALUNO_DISCIPLINA AS AD ON D.codigo = AD.codigo_disciplina
JOIN
    ALUNO AS A ON AD.matricula_aluno = A.matricula
WHERE
    D.codigo = 10010; -- Substitua pelo código da disciplina desejada
    
    
-- 4.2 Dado uma disciplina, deseja-se saber quais são os pré-requisitos da disciplina:
USE Equipe521461;
SELECT
    D.nome AS Nome_Disciplina,
    PR.nome AS Pre_Requisito
FROM
    DISCIPLINA AS D
JOIN
    PRE_REQUISITO_DISCIPLINA AS PRD ON D.codigo = PRD.codigo_disciplina
JOIN
    DISCIPLINA AS PR ON PRD.codigo_pre_requisito = PR.codigo
WHERE
    D.codigo = 10010; -- Substitua pelo código da disciplina desejada
    

-- 4.3 Dado uma disciplina, deseja-se saber quais disciplinas para as quais a mesma é pré-requisito:
USE Equipe521461;
SELECT
    PR.nome AS Nome_Disciplina_Pre_Requisito,
    D.nome AS Disciplina_Que_Requer
FROM
    DISCIPLINA AS PR -- PR aqui é a disciplina que é pré-requisito
JOIN
    PRE_REQUISITO_DISCIPLINA AS PRD ON PR.codigo = PRD.codigo_pre_requisito
JOIN
    DISCIPLINA AS D ON PRD.codigo_disciplina = D.codigo
WHERE
    PR.codigo = 10020; -- Substitua pelo código da disciplina que é pré-requisito (ex: Estrutura de Dados)
    
    
-- 5.1 Dado um orientador, deseja-se saber quais alunos orientandos daquele orientador:
USE Equipe521461;
SELECT
    P.nome_completo AS Nome_Orientador,
    A.matricula,
    A.nome AS Nome_Aluno_Pos_Graduacao,
    APG.formacao_basica
FROM
    PROFESSOR AS P
JOIN
    ALUNO_POS_GRADUACAO AS APG ON P.siape = APG.siape_orientador
JOIN
    ALUNO AS A ON APG.matricula_aluno = A.matricula
WHERE
    P.siape = 1001; -- Substitua pelo SIAPE do orientador desejado
    
    
-- 5.2 Dado um orientador, deseja-se saber quais são as disciplinas dadas pelo orientador:
USE Equipe521461;
SELECT
    P.nome_completo AS Nome_Professor,
    D.nome AS Nome_Disciplina,
    D.numero_creditos AS Creditos
FROM
    PROFESSOR AS P
JOIN
    MINISTRA_DISCIPLINA AS MD ON P.siape = MD.siape_professor
JOIN
    DISCIPLINA AS D ON MD.codigo_disciplina = D.codigo
WHERE
    P.siape = 1001; -- Substitua pelo SIAPE do professor/orientador desejado


-- 5.3 Dado um orientador, deseja-se saber qual é o total de créditos das disciplinas do mesmo:
USE Equipe521461;
SELECT
    P.nome_completo AS Nome_Professor,
    SUM(D.numero_creditos) AS Total_Creditos_Disciplinas_Ministradas
FROM
    PROFESSOR AS P
JOIN
    MINISTRA_DISCIPLINA AS MD ON P.siape = MD.siape_professor
JOIN
    DISCIPLINA AS D ON MD.codigo_disciplina = D.codigo
WHERE
    P.siape = 1001 -- Substitua pelo SIAPE do professor/orientador desejado
GROUP BY
    P.nome_completo;
