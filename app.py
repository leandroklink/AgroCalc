from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__) #criando aplicação Flask
database.criar_banco()

#Rota principal (Dashboard)
@app.route("/")
def home():
    return render_template("index.html")

# página de custos
@app.route('/custos', methods=['GET', 'POST'])
def custos():

    resultado = None

    if request.method == 'POST':
        try:
            cf_input = request.form.get("custo_fixo")
            cv_input = request.form.get("custo_variavel")
            qd_input = request.form.get("quantidade")

            cf = float(cf_input)
            cv = float(cv_input)
            qd = float(qd_input)

            resultado = cf + (cv * qd)

            database.salvar_calculo(
                cf,
                cv,
                qd,
                resultado
            )

        except ValueError:
            return render_template(
                'custos.html',
                erro='Preencha todos os campos corretamente.',
                custo_fixo=cf_input,
                custo_variavel=cv_input,
                quantidade=qd_input
            )

    busca = database.buscar_calculos()

    return render_template(
        'custos.html',
        resultado=resultado,
        busca=busca
    ) 

#deletar calculo da tela de custos
@app.route('/deletar-calculo', methods=['POST'])
def deletar_calculo():
    id = int(request.form.get('id'))
    database.deletar_calculo(id)
    return redirect(url_for('custos'))




#alterar calculo tela de custos
@app.route('/editar-calculo/<int:id>')
def editar_calculo(id):
    calculo = database.buscar_calculo_por_id(id)
    return render_template(
        'editar_calculo.html',
        calculo=calculo
    )

#finalizar edição
@app.route('/salvar-edicao', methods=['POST'])
def salvar_edicao():

    id = int(request.form.get('id'))

    cf = float(request.form.get('custo_fixo'))
    cv = float(request.form.get('custo_variavel'))
    qd = float(request.form.get('quantidade'))

    resultado = cf + (cv * qd)

    database.atualizar_calculo(
        id,
        cf,
        cv,
        qd,
        resultado
    )

    return redirect(url_for('custos'))


#página financiamento
@app.route("/financiamento")
def financiamento():
    return render_template("financiamento.html")

# Página conversor
@app.route("/conversor")
def conversor():
    return render_template("conversor.html")


# Página talhões
@app.route("/talhoes")
def talhoes():
    return render_template("talhoes.html")


# Página fertilizantes
@app.route("/fertilizantes")
def fertilizantes():
    return render_template("fertilizante.html")


# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)