from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
import database

app = Flask(__name__) #criando aplicação Flask
app.secret_key = '123456'
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
            flash(f'Cálculo salvo! Resultado: R$ {resultado}')
            return redirect(url_for('custos'))
            

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


@app.route('/financiamento', methods=['GET', 'POST'])
def financiamento():

    parcela = None
    total_pago = None
    juros_total = None

    if request.method == 'POST':
        try:
            valor_input = request.form.get("valor_financiado")

            taxa_input = request.form.get("taxa")

            parcelas_input = request.form.get("parcelas")

            valor = float(valor_input)
            taxa = float(taxa_input)
            parcelas = int(parcelas_input)
            if parcelas > 1000:
                return render_template('financiamento.html',
                    erro='Número de parcelas muito alto.')

            taxa = taxa / 100

            potencia = (1 + taxa) ** parcelas

            numerador = taxa * potencia
            denominador = potencia - 1

            parcela = (valor *(numerador / denominador))
            total_pago = parcela * parcelas
            juros_total = (total_pago - valor)

            saldo = valor
            
            amortizacao = []

            for numero in range(1, parcelas + 1):

                juros = saldo * taxa

                amortizacao_mes = parcela - juros

                saldo = saldo - amortizacao_mes

                saldo = round(saldo, 2)
                saldo = max(0, saldo)

                amortizacao.append((
                    numero,
                    juros,
                    amortizacao_mes,
                    saldo
                ))

            return render_template(
                'financiamento.html',
                parcela=parcela,
                total_pago=total_pago,
                juros_total=juros_total,
                amortizacao=amortizacao
            )
        except ValueError:

            return render_template(
                'financiamento.html',
                erro='Preencha os dados corretamente.'
            )
        except OverflowError:
            return render_template(
                'financiamento.html',
                erro='Valores muito altos para realizar o cálculo.'
            )

    return render_template(
        'financiamento.html',
        parcela=parcela,
        total_pago=total_pago,
        juros_total=juros_total
    )

# Página fertilizantes
@app.route('/fertilizante', methods = ['GET','POST'])
def fertilizante():

    area = None
    dose = None
    total = None
    totalTol = None

    if request.method == 'POST':
        try:
            area_input = request.form.get("area")
            dose_input = request.form.get("dose")
            area = float(area_input)
            dose = float(dose_input)

            total = area * dose
            totalTol = total / 1000
            return render_template(
                'fertilizante.html',
                total=total,
                totalTol=totalTol)
        
        except ValueError:
            return render_template(
                'fertilizante.html',
                erro='Preencha todos os campos corretamente.',
                area=area_input,
                dose=dose_input)
        
    return render_template(
        'fertilizante.html',
        area=area,
        dose=dose,
        total=total,
        totalTol=totalTol)


# Página conversor
@app.route("/conversor", methods = ['GET','POST'])
def conversor():

    valor = None
    tipo = None
    resultado = None

    if request.method == 'POST':
        try:
            valor_input = request.form.get("valor")
            tipo = request.form.get("tipo")
            valor = float(valor_input)

            if tipo == "kg_ton":
                resultado = valor / 1000
            elif tipo == "ton_kg":
                resultado = valor * 1000
            elif tipo == "ha_alq":
                resultado = valor / 2.42

            return render_template(
                'conversor.html',
                resultado=resultado)
        
        except ValueError:
            return render_template(
                'conversor.html',
                erro='Preencha todos os campos corretamente.',
                valor=valor_input,
                tipo=tipo)
        
    return render_template(
        'conversor.html',
        valor=valor,
        tipo=tipo,
        resultado=resultado)





#Rota de talhões
@app.route("/talhoes", methods = ['GET','POST'])
def talhoes():

    producao = None
    if request.method == 'POST':
        try:
            nome = request.form.get("nome_talhao")
            area_input = request.form.get("area")
            produtividade_input = request.form.get("produtividade")


            area = float(area_input)
            produtividade = float(produtividade_input)

            producao = area * produtividade

            database.salvar_talhao(
                nome,
                area,
                produtividade,
                producao   
            )
            flash(f'Talhão {nome} cadastrado! Produção estimada: {producao:.2f} sacas.')
            return redirect(url_for('talhoes'))
            

        except ValueError:
            return render_template(
                'talhoes.html',
                erro='Preencha todos os campos corretamente.',
                nome=nome,
                area=area,
                produtividade=produtividade,
            )

    busca = database.buscar_talhoes()

    return render_template(
        'talhoes.html',
        busca=busca
    ) 


#deletar calculo da tela de talhoes
@app.route('/deletar-talhao', methods=['POST'])
def deletar_talhao():
    id = int(request.form.get('id'))
    database.deletar_talhao(id)
    return redirect(url_for('talhoes'))


#alterar calculo tela de talhoes
@app.route('/editar-talhao/<int:id>')
def editar_talhao(id):
    talhao = database.buscar_talhao_por_id(id)
    return render_template(
        'editar_talhao.html',
        talhao=talhao
    )

#finalizar edição
@app.route('/salvar-edicao-talhao', methods=['POST'])
def salvar_edicao_talhao():

    id = int(request.form.get('id'))
    nome = request.form.get("nome_talhao")
    area_input = request.form.get("area")
    produtividade_input = request.form.get("produtividade")

    area = float(area_input)
    produtividade = float(produtividade_input)

    producao = area * produtividade
    
    database.atualizar_talhao(
        id,
        nome,
        area,
        produtividade,
        producao  
    )
    return redirect(url_for('talhoes'))


# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)
