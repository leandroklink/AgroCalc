import sqlite3

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
                    resultado
                FROM calculos
""")
    busca = cursor.fetchall()
    conexao.close()
    return busca
