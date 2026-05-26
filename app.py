from flask import Flask, render_template, request
import database

app = Flask(__name__) #criando aplicação Flask
database.criar_banco()

#Rota principal (Dashboard)
@app.route("/")
def home():
    return render_template("index.html")

#página de custos
@app.route('/custos', methods=['GET', 'POST'])
def custos():

    if request.method == 'POST':
        try:
            cf_input = request.form.get("custo_fixo")
            cv_input = request.form.get("custo_variavel")
            qd_input = request.form.get("quantidade")

            cf = float(cf_input)
            cv = float(cv_input)
            qd = float(qd_input)

            resultado = cf + (cv * qd)
            database.salvar_calculo(cf, cv, qd, resultado)
            return render_template(
                'custos.html',
                resultado=resultado
            )

        except ValueError:
            return render_template(
                'custos.html',
                erro='Preencha todos os campos corretamente.',
                    custo_fixo=cf_input,
                    custo_variavel=cv_input,
                    quantidade=qd_input
                
            )

    return render_template('custos.html')   

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