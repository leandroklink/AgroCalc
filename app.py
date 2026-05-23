from flask import Flask, render_template

app = Flask(__name__) #criando aplicação Flask

#Rota principal (Dashboard)
@app.route("/")
def home():
    return render_template("index.html")

#página de custos
@app.route("/custos")
def custos():
    return render_template("custo.html")

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