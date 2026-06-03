import sqlite3
from datetime import datetime

def conectar():
    conexao = sqlite3.connect('banco.db')
    return conexao

#parte de custos
def criar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        custo_fixo REAL,
        custo_variavel REAL,
        quantidade REAL,
        resultado REAL,
        data_calculo DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS talhoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        area REAL,
        produtividade REAL,
        producao REAL,
        data_talhao DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS atividades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT,
        data_atividade DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL, 
        senha TEXT NOT NULL
    )
    """) #unique no email para não cadastrar mais que um usuário no mesmo sistema
    conexao.commit()
    conexao.close()




def salvar_calculo(custo_fixo, custo_variavel, quantidade, resultado):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO calculos
        (
            custo_fixo,
            custo_variavel,
            quantidade,
            resultado
        )
        VALUES (?, ?, ?, ?)
    """, (
        custo_fixo,
        custo_variavel,
        quantidade,
        resultado
    ))

    conexao.commit()
    conexao.close()

def buscar_calculos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            custo_fixo,
            custo_variavel,
            quantidade,
            resultado,
            data_calculo,
            id
        FROM calculos
        ORDER BY id DESC
        LIMIT 20
    """)

    busca = cursor.fetchall()

    calculos_formatados = []

    for calculo in busca:
        data_formatada = datetime.strptime(
            calculo[4],
            '%Y-%m-%d %H:%M:%S'
        ).strftime('%d/%m/%Y às %H:%M')

        calculos_formatados.append((
            calculo[0],
            calculo[1],
            calculo[2],
            calculo[3],
            data_formatada,
            calculo[5]
        ))

    conexao.close()

    return calculos_formatados


def buscar_calculo_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM calculos
        WHERE id = ?
    """, (id,))
    busca = cursor.fetchone()

    conexao.close()
    return busca


def deletar_calculo(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM calculos
        WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()


def atualizar_calculo(id, cf, cv, qd, resultado):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE calculos
        SET
            custo_fixo = ?,
            custo_variavel = ?,
            quantidade = ?,
            resultado = ?
        WHERE id = ?
    """, (
        cf,
        cv,
        qd,
        resultado,
        id
    ))
    conexao.commit()
    conexao.close()





#parte de talhoes


def salvar_talhao(nome, area, produtividade, producao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO talhoes
        (
            nome, area, produtividade, producao
        )
        VALUES (?, ?, ?, ?)
    """, (
        nome, area, produtividade, producao
    ))

    conexao.commit()
    conexao.close()

def buscar_talhoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id, nome, area, produtividade, data_talhao, producao
            FROM talhoes
        ORDER BY id DESC
        LIMIT 20
    """)

    busca = cursor.fetchall()

    talhoes_formatados = []

    for talhao in busca:
        data_formatada_t = datetime.strptime(
            talhao[4],
            '%Y-%m-%d %H:%M:%S'
        ).strftime('%d/%m/%Y às %H:%M')

        talhoes_formatados.append((
            talhao[0],
            talhao[1],
            talhao[2],
            talhao[3],
            data_formatada_t,
            talhao[5]
        ))

    conexao.close()

    return talhoes_formatados


def buscar_talhao_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM talhoes
        WHERE id = ?
    """, (id,))
    busca = cursor.fetchone()

    conexao.close()
    return busca


def deletar_talhao(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM talhoes
        WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()


def atualizar_talhao(id, nome, area, produtividade, producao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE talhoes
        SET
            nome = ?,
            area = ?,
            produtividade = ?,
            producao = ?
        WHERE id = ?
    """, (
        nome, area, produtividade, producao, id
    ))
    conexao.commit()
    conexao.close()


#rotas do index

#Producao Total
def producao_total():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT SUM(producao)
        FROM talhoes
    """)

    total = cursor.fetchone()[0]

    conexao.close()

    return total or 0

def custo_operacional():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT SUM(resultado)
        FROM calculos
    """)
    total = cursor.fetchone()[0]
    conexao.close()
    return total or 0


#soma da quantidade de talhoes
def total_talhoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM talhoes
    """)

    total = cursor.fetchone()[0]

    conexao.close()

    return total or 0


#soma da área de talhões
def area_total():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT SUM(area)
        FROM talhoes
    """)

    total = cursor.fetchone()[0]

    conexao.close()

    return total or 0

#salvar atividade
def registrar_atividade(descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO atividades (descricao)
        VALUES (?)
    """, (descricao,))

    conexao.commit()
    conexao.close()


#exibição de historico
def buscar_atividades():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT descricao
        FROM atividades
        ORDER BY id DESC
        LIMIT 10
    """)

    atividades = cursor.fetchall()

    conexao.close()

    return atividades



#login de usuários


def salvar_usuario(nome, email, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (
            nome,
            email,
            senha
        )
        VALUES (?, ?, ?)
    """, (
        nome,
        email,
        senha
    ))
    conexao.commit()
    conexao.close()



def buscar_usuario_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM usuarios WHERE
        email = ? """,(email,))
    usuario = cursor.fetchone()
    conexao.close()

    return usuario

