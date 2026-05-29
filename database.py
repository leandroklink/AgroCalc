import sqlite3
from datetime import datetime

def conectar():
    conexao = sqlite3.connect('banco.db')
    return conexao

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