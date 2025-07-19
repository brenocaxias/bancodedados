-- SQL Script para Criação do Banco de Dados UniUFC-BD
-- Nome do BD: Equipe521461
-- Ferramenta CASE: MySQL Workbench
-- Versão do MySQL: 5.7 ou superior

-- Desabilitar verificação de chaves estrangeiras temporariamente para evitar problemas de ordem
SET FOREIGN_KEY_CHECKS = 0;
-- 1. Criação do Banco de Dados
CREATE DATABASE IF NOT EXISTS Equipe521461;
USE Equipe521461;

-- 2. Tabela: DEPARTAMENTO

CREATE TABLE IF NOT EXISTS DEPARTAMENTO (
    codigo INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    PRIMARY KEY (codigo)
);

-- 3. Tabela: CURSO

CREATE TABLE IF NOT EXISTS CURSO (
    codigo INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    quantidade_minima_creditos INT NOT NULL,
    codigo_departamento INT NOT NULL,
    PRIMARY KEY (codigo),
    FOREIGN KEY (codigo_departamento) REFERENCES DEPARTAMENTO (codigo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- 4. Tabela: PROFESSOR

CREATE TABLE IF NOT EXISTS PROFESSOR (
    siape INT NOT NULL,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    data_ingresso DATE NOT NULL,
    codigo_departamento INT NOT NULL,
    PRIMARY KEY (siape),
    FOREIGN KEY (codigo_departamento) REFERENCES DEPARTAMENTO (codigo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT 
);

-- 5. Tabela: DISCIPLINA

CREATE TABLE IF NOT EXISTS DISCIPLINA (
    codigo INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    ementa TEXT,
    numero_creditos INT NOT NULL,
    tipo ENUM('obrigatoria', 'optativa') NOT NULL,
    codigo_curso INT NOT NULL,
    PRIMARY KEY (codigo),
    FOREIGN KEY (codigo_curso) REFERENCES CURSO (codigo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- 6. Tabela: ALUNO

CREATE TABLE IF NOT EXISTS ALUNO (
    matricula INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    tipo_aluno ENUM('graduacao', 'pos_graduacao') NOT NULL,
    codigo_curso INT NOT NULL,
    PRIMARY KEY (matricula),
    FOREIGN KEY (codigo_curso) REFERENCES CURSO (codigo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT 
);

-- 7. Tabela: ALUNO_GRADUACAO (Subclasse de ALUNO)

CREATE TABLE IF NOT EXISTS ALUNO_GRADUACAO (
    matricula_aluno INT NOT NULL,
    ano_ingresso INT NOT NULL,
    PRIMARY KEY (matricula_aluno),
    FOREIGN KEY (matricula_aluno) REFERENCES ALUNO (matricula)
        ON UPDATE CASCADE
        ON DELETE CASCADE 
);

-- 8. Tabela: ALUNO_POS_GRADUACAO (Subclasse de ALUNO)

CREATE TABLE IF NOT EXISTS ALUNO_POS_GRADUACAO (
    matricula_aluno INT NOT NULL,
    formacao_basica TEXT,
    siape_orientador INT NOT NULL,
    PRIMARY KEY (matricula_aluno),
    FOREIGN KEY (matricula_aluno) REFERENCES ALUNO (matricula)
        ON UPDATE CASCADE
        ON DELETE CASCADE, 
    FOREIGN KEY (siape_orientador) REFERENCES PROFESSOR (siape)
        ON UPDATE CASCADE
        ON DELETE RESTRICT 
);

-- 9. Tabela: USUARIO_ACESSO (para controle de acesso ao sistema)

CREATE TABLE IF NOT EXISTS USUARIO_ACESSO (
    login VARCHAR(50) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    nivel_acesso ENUM('DBA', 'funcionario', 'aluno', 'professor') NOT NULL,
    PRIMARY KEY (login)
);

-- 10. Tabela: EMAIL_PROFESSOR (para múltiplos e-mails de um professor)

CREATE TABLE IF NOT EXISTS EMAIL_PROFESSOR (
    id_email INT AUTO_INCREMENT NOT NULL,
    siape_professor INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_email),
    FOREIGN KEY (siape_professor) REFERENCES PROFESSOR (siape)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- 11. Tabela: TELEFONE_PROFESSOR (para múltiplos telefones de um professor)

CREATE TABLE IF NOT EXISTS TELEFONE_PROFESSOR (
    id_telefone INT AUTO_INCREMENT NOT NULL,
    siape_professor INT NOT NULL,
    numero VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_telefone),
    FOREIGN KEY (siape_professor) REFERENCES PROFESSOR (siape)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- 12. Tabela: TELEFONE_ALUNO (para múltiplos telefones de um aluno)

CREATE TABLE IF NOT EXISTS TELEFONE_ALUNO (
    id_telefone INT AUTO_INCREMENT NOT NULL,
    matricula_aluno INT NOT NULL,
    numero VARCHAR(20) NOT NULL,
    descricao VARCHAR(50),
    PRIMARY KEY (id_telefone),
    FOREIGN KEY (matricula_aluno) REFERENCES ALUNO (matricula)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- 13. Tabela Associativa: PRE_REQUISITO_DISCIPLINA (para N:M recursivo de DISCIPLINA)

CREATE TABLE IF NOT EXISTS PRE_REQUISITO_DISCIPLINA (
    codigo_disciplina INT NOT NULL,
    codigo_pre_requisito INT NOT NULL,
    PRIMARY KEY (codigo_disciplina, codigo_pre_requisito),
    FOREIGN KEY (codigo_disciplina) REFERENCES DISCIPLINA (codigo)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (codigo_pre_requisito) REFERENCES DISCIPLINA (codigo)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- 14. Tabela Associativa: MINISTRA_DISCIPLINA (para N:M entre PROFESSOR e DISCIPLINA)

CREATE TABLE IF NOT EXISTS MINISTRA_DISCIPLINA (
    siape_professor INT NOT NULL,
    codigo_disciplina INT NOT NULL,
    PRIMARY KEY (siape_professor, codigo_disciplina),
    FOREIGN KEY (siape_professor) REFERENCES PROFESSOR (siape)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (codigo_disciplina) REFERENCES DISCIPLINA (codigo)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- 15. Tabela Associativa: ALUNO_DISCIPLINA (para N:M entre ALUNO e DISCIPLINA)

CREATE TABLE IF NOT EXISTS ALUNO_DISCIPLINA (
    matricula_aluno INT NOT NULL,
    codigo_disciplina INT NOT NULL,
    media_final DECIMAL(4,2), 
    frequencia DECIMAL(5,2),
    PRIMARY KEY (matricula_aluno, codigo_disciplina),
    FOREIGN KEY (matricula_aluno) REFERENCES ALUNO (matricula)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (codigo_disciplina) REFERENCES DISCIPLINA (codigo)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
-- 1.1 Dado o número (matrícula) do aluno, deseja-se saber em quais disciplinas está atualmente matriculado:
USE Equipe521461;
SELECT
    A.NOME AS NOME_ALUNO,
    D.NOME AS NOME_DISCIPLINA,
    AD.MEDIA_FINAL AS MEDIA_FINAL,
    AD.FREQUENCIA AS FREQUENCIA
FROM
    ALUNO AS A
JOIN
    ALUNO_DISCIPLINA AS AD ON A.MATRICULA = AD.MATRICULA_ALUNO
JOIN
    DISCIPLINA AS D ON AD.CODIGO_DISCIPLINA = D.CODIGO
WHERE
    A.MATRICULA = 20230001; -- Substitua pela matrícula do aluno desejado
    
    
-- 1.2 Dado o número (matrícula) do aluno, deseja-se saber quais disciplinas já concluiu:
USE Equipe521461;
SELECT
    A.NOME AS NOME_ALUNO,
    D.NOME AS NOME_DISCIPLINA,
    AD.MEDIA_FINAL AS MEDIA_FINAL,
    AD.FREQUENCIA AS FREQUENCIA
FROM
    ALUNO AS A
JOIN
    ALUNO_DISCIPLINA AS AD ON A.MATRICULA = AD.MATRICULA_ALUNO
JOIN
    DISCIPLINA AS D ON AD.CODIGO_DISCIPLINA = D.CODIGO
WHERE
    A.MATRICULA = 20230001 -- Substitua pela matrícula do aluno desejado
    AND AD.MEDIA_FINAL >= 7.0;
    

-- 1.3 Dado o número (matrícula) do aluno, deseja-se saber qual o curso deste aluno:
USE Equipe521461;
SELECT
    A.NOME AS NOME_ALUNO,
    C.NOME AS NOME_CURSO,
    C.CODIGO AS CODIGO_CURSO
FROM
    ALUNO AS A
JOIN
    CURSO AS C ON A.CODIGO_CURSO = C.CODIGO
WHERE
    A.MATRICULA = 20230001; -- Substitua pela matrícula do aluno desejado
    
    
-- 1.4 Dado o número (matrícula) do aluno, deseja-se saber os dados pessoais sobre o aluno:
USE Equipe521461;
SELECT
    A.MATRICULA,
    A.NOME,
    A.ENDERECO,
    A.TIPO_ALUNO,
    C.NOME AS NOME_CURSO -- Inclui o nome do curso para contexto
FROM
    ALUNO AS A
JOIN
    CURSO AS C ON A.CODIGO_CURSO = C.CODIGO
WHERE
    A.MATRICULA = 20230001; -- Substitua pela matrícula do aluno desejado
    

-- 2.1 Dado o código de um departamento, deseja-se saber quais cursos estão sob a responsabilidade do departamento:
USE Equipe521461;
SELECT
    D.NOME AS NOME_DEPARTAMENTO,
    C.NOME AS NOME_CURSO,
    C.CODIGO AS CODIGO_CURSO,
    C.QUANTIDADE_MINIMA_CREDITOS AS CREDITOS_MINIMOS
FROM
    DEPARTAMENTO AS D
JOIN
    CURSO AS C ON D.CODIGO = C.CODIGO_DEPARTAMENTO
WHERE
    D.CODIGO = 100; -- Substitua pelo código do departamento desejado
    
    
-- 2.2 Dado o código de um departamento, deseja-se saber detalhes sobre o departamento:
USE Equipe521461;
SELECT
    CODIGO AS CODIGO_DEPARTAMENTO,
    NOME AS NOME_DEPARTAMENTO
FROM
    DEPARTAMENTO
WHERE
    CODIGO = 100; -- Substitua pelo código do departamento desejado
    
    
-- 3.1 Dado um curso, deseja-se saber quais são as disciplinas obrigatórias do curso:
USE Equipe521461;
SELECT
    C.NOME AS NOME_CURSO,
    D.NOME AS NOME_DISCIPLINA,
    D.NUMERO_CREDITOS AS CREDITOS,
    D.TIPO
FROM
    CURSO AS C
JOIN
    DISCIPLINA AS D ON C.CODIGO = D.CODIGO_CURSO
WHERE
    C.CODIGO = 10 -- Substitua pelo código do curso desejado
    AND D.TIPO = 'obrigatoria';
    
    
-- 3.2 Dado um curso, deseja-se saber quais são as disciplinas optativas do curso:
USE Equipe521461;
SELECT
    C.NOME AS NOME_CURSO,
    D.NOME AS NOME_DISCIPLINA,
    D.NUMERO_CREDITOS AS CREDITOS,
    D.TIPO
FROM
    CURSO AS C
JOIN
    DISCIPLINA AS D ON C.CODIGO = D.CODIGO_CURSO
WHERE
    C.CODIGO = 10 -- Substitua pelo código do curso desejado
    AND D.TIPO = 'optativa';
    
    
-- 3.3 Dado um curso, deseja-se saber quais são os alunos desse curso:
USE Equipe521461;
SELECT
    C.NOME AS NOME_CURSO,
    A.MATRICULA,
    A.NOME AS NOMME_ALUNO,
    A.TIPO_ALUNO
FROM
    CURSO AS C
JOIN
    ALUNO AS A ON C.CODIGO = A.CODIGO_CURSO
WHERE
    C.CODIGO = 10; -- Substitua pelo código do curso desejado
    
    
-- 3.4 Dado um curso, deseja-se saber quais alunos deste já fizeram todas as disciplinas obrigatórias:
USE Equipe521461;
SELECT
    A.MATRICULA,
    A.NOME AS NOME_ALUNO,
    C.NOME AS NOME_CURSO
FROM
    ALUNO AS A
JOIN
    CURSO AS C ON A.CODIGO_CURSO = C.CODIGO
WHERE
    C.CODIGO = 10 -- Substitua pelo código do curso desejado
    AND A.TIPO_ALUNO = 'graduacao' -- Assumindo que apenas alunos de graduação têm "todas as obrigatórias"
    AND (
        SELECT COUNT(DISTINCT D.codigo)
        FROM DISCIPLINA AS D
        WHERE D.CODIGO_CURSO = C.CODIGO AND D.TIPO = 'obrigatoria'
    ) = (
        SELECT COUNT(DISTINCT AD.CODIGO_DISCIPLINA) 
        FROM ALUNO_DISCIPLINA AS AD
        JOIN DISCIPLINA AS D2 ON AD.CODIGO_DISCIPLINA = D2.CODIGO
        WHERE AD.MATRICULA_ALUNO = A.MATRICULA
        AND D2.CODIGO_CURSO = C.CODIGO
        AND D2.TIPO = 'obrigatoria'
        AND AD.MEDIA_FINAL >= 7.0 -- Critério de conclusão
    );


-- 3.5 Dado um curso, deseja-se saber quais alunos não fizeram nenhuma disciplina optativa:
USE Equipe521461;
SELECT
    A.MATRICULA,
    A.NOME AS NOME_ALUNO,
    C.NOME AS NOME_CURSO
FROM
    ALUNO AS A
JOIN
    CURSO AS C ON A.CODIGO_CURSO = C.CODIGO
WHERE
    C.CODIGO = 10 -- Substitua pelo código do curso desejado
    AND A.MATRICULA NOT IN (
        SELECT AD.MATRICULA_ALUNO
        FROM ALUNO_DISCIPLINA AS AD
        JOIN DISCIPLINA AS D ON AD.CODIGO_DISCIPLINA = D.CODIGO
        WHERE D.CODIGO_CURSO = C.CODIGO AND D.TIPO = 'optativa'
    );
    
    
-- 4.1 Dado uma disciplina, deseja-se saber quais alunos foram matriculados na disciplina:
USE Equipe521461;
SELECT
    D.NOME AS NOME_DISCIPLINA,
    A.MATRICULA,
    A.NOME AS NOME_ALUNO,
    AD.MEDIA_FINAL,
    AD.FREQUENCIA
FROM
    DISCIPLINA AS D
JOIN
    ALUNO_DISCIPLINA AS AD ON D.CODIGO = AD.CODIGO_DISCIPLINA
JOIN
    ALUNO AS A ON AD.MATRICULA_ALUNO = A.MATRICULA
WHERE
    D.CODIGO = 10010; -- Substitua pelo código da disciplina desejada
    
    
-- 4.2 Dado uma disciplina, deseja-se saber quais são os pré-requisitos da disciplina:
USE Equipe521461;
SELECT
    D.NOME AS NOME_DISCIPLINA,
    PR.NOME AS PRE_REQUISITO
FROM
    DISCIPLINA AS D
JOIN
    PRE_REQUISITO_DISCIPLINA AS PRD ON D.CODIGO = PRD.CODIGO_DISCIPLINA
JOIN
    DISCIPLINA AS PR ON PRD.CODIGO_PRE_REQUISITO = PR.CODIGO
WHERE
    D.CODIGO = 10010; -- Substitua pelo código da disciplina desejada
    

-- 4.3 Dado uma disciplina, deseja-se saber quais disciplinas para as quais a mesma é pré-requisito:
USE Equipe521461;
SELECT
    PR.NOME AS NOME_DISCIPLINA_PRE_REQUISITO,
    D.NOME AS DISCIPLINA_QUE_REQUER
FROM
    DISCIPLINA AS PR -- PR aqui é a disciplina que é pré-requisito
JOIN
    PRE_REQUISITO_DISCIPLINA AS PRD ON PR.CODIGO = PRD.CODIGO_PRE_REQUISITO
JOIN
    DISCIPLINA AS D ON PRD.CODIGO_DISCIPLINA = D.CODIGO
WHERE
    PR.CODIGO = 10020; -- Substitua pelo código da disciplina que é pré-requisito (ex: Estrutura de Dados)
    
    
-- 5.1 Dado um orientador, deseja-se saber quais alunos orientandos daquele orientador:
USE Equipe521461;
SELECT
    P.NOME_COMPLETO AS NOME_ORIENTADOR,
    A.MATRICULA,
    A.NOME AS NOME_ALUNO_POS_GRADUACAO,
    APG.FORMACAO_BASICA
FROM
    PROFESSOR AS P
JOIN
    ALUNO_POS_GRADUACAO AS APG ON P.SIAPE = APG.SIAPE_ORIENTADOR
JOIN
    ALUNO AS A ON APG.MATRICULA_ALUNO = A.MATRICULA
WHERE
    P.SIAPE = 1001; -- Substitua pelo SIAPE do orientador desejado
    
    
-- 5.2 Dado um orientador, deseja-se saber quais são as disciplinas dadas pelo orientador:
USE Equipe521461;
SELECT
    P.NOME_COMPLETO AS NOME_PROFESSOR,
    D.NOME AS NOME_DISCIPLINA,
    D.NUMERO_CREDITOS AS CREDITOS
FROM
    PROFESSOR AS P
JOIN
    MINISTRA_DISCIPLINA AS MD ON P.SIAPE = MD.SIAPE_PROFESSOR
JOIN
    DISCIPLINA AS D ON MD.CODIGO_DISCIPLINA = D.CODIGO
WHERE
    P.SIAPE = 1001; -- Substitua pelo SIAPE do professor/orientador desejado


-- 5.3 Dado um orientador, deseja-se saber qual é o total de créditos das disciplinas do mesmo:
USE Equipe521461;
SELECT
    P.NOME_COMPLETO AS NOME_PROFESSOR,
    SUM(D.NUMERO_CREDITOS) AS TOTAL_CREDITOS_DISCIPLINAS_MINISTRADAS
FROM
    PROFESSOR AS P
JOIN
    MINISTRA_DISCIPLINA AS MD ON P.SIAPE = MD.SIAPE_PROFESSOR
JOIN
    DISCIPLINA AS D ON MD.CODIGO_DISCIPLINA = D.CODIGO
WHERE
    P.SIAPE = 1001 -- Substitua pelo SIAPE do professor/orientador desejado
GROUP BY
    P.NOME_COMPLETO;


-- Reabilitar verificação de chaves estrangeiras
SET FOREIGN_KEY_CHECKS = 1;