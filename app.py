from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

import os
from werkzeug.security import check_password_hash #criptografia de senha
from werkzeug.security import generate_password_hash #criptografia de senha
import database #importacao de API de banco de dados

app = Flask(__name__) #criando aplicação Flask
app.secret_key = os.environ.get("SECRET_KEY") #definindo chave secreta de criptografia configurada no render
database.criar_banco()



# página de custos
@app.route('/custos', methods=['GET', 'POST'])
def custos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    resultado = None

    if request.method == 'POST': # define os metodos como GET ou POST, se for get apenas apresenta, se for post importa os dados e calcula
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
            ) #salva os dados na database
            database.registrar_atividade(
                f'Calculo realizado'
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
@app.route('/deletar-calculo', methods=['POST']) #atraves de metodo post realiza o delete do banco do calculo buscado
def deletar_calculo():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    id = int(request.form.get('id'))
    database.deletar_calculo(id)
    database.registrar_atividade(
    f'Calculo deletado.'
    )
    return redirect(url_for('custos'))




#alterar calculo tela de custos
@app.route('/editar-calculo/<int:id>') #leva o usuario a tela de edição de calculos
def editar_calculo(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    calculo = database.buscar_calculo_por_id(id)

    return render_template(
        'editar_calculo.html',
        calculo=calculo
    )

#finalizar edição
@app.route('/salvar-edicao', methods=['POST'])
def salvar_edicao():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

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
    database.registrar_atividade(
    f'Calculo atualizado'
    )
    return redirect(url_for('custos'))


@app.route('/financiamento', methods=['GET', 'POST']) # define os metodos como GET ou POST, se for get apenas apresenta, se for post importa os dados e calcula o financiamento
def financiamento():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

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

            taxa = taxa / 100 #calculo da taxa

            potencia = (1 + taxa) ** parcelas #calcula as parcelas

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
            database.registrar_atividade(
            'Financiamento calculado'
            )

            return render_template(
                'financiamento.html',
                parcela=parcela,
                total_pago=total_pago,
                juros_total=juros_total,
                amortizacao=amortizacao
            )
        #abaixo tratamento de erros de valor ou overflow
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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

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

            total = area * dose #calculos do fertilizante
            totalTol = total / 1000

            database.registrar_atividade(
                'Fertilizante calculado')
            
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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    valor = None
    tipo = None
    resultado = None

    if request.method == 'POST':
        try:
            valor_input = request.form.get("valor")
            tipo = request.form.get("tipo")
            valor = float(valor_input)
            #abaixo calculos de conversao para determinada escolha non post
            if tipo == "kg_ton":
                resultado = valor / 1000
            elif tipo == "ton_kg":
                resultado = valor * 1000
            elif tipo == "ha_alq":
                resultado = valor / 2.42
            database.registrar_atividade(
                'Conversão calculada')

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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    producao = None
    if request.method == 'POST':
        try:
            nome = request.form.get("nome_talhao")
            area_input = request.form.get("area")
            produtividade_input = request.form.get("produtividade")


            area = float(area_input) #em todos os posts existem essas conversões porque quando os dados são importados da pagina vem como string, e são convertidos para float ou int só depois, porque se ocorre
                                     #algum erro ele apenas retorna os valores em string novamente, essa conversão é usada para os calculos ou registros no banco de dados
            produtividade = float(produtividade_input)

            producao = area * produtividade # calculo de producao

            database.salvar_talhao(
                nome,
                area,
                produtividade,
                producao   
            ) #salvando talhao na database
            database.registrar_atividade(
                'Financiamento calculado'
            )#esse regfistrar atividadade registra nessa tabelas as ações feitas no momento e exibe as 5 ultimas no index.html no dashboard

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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    id = int(request.form.get('id'))
    database.deletar_talhao(id)
    database.registrar_atividade(
        f'Talhão de id {id} deletado'
    )
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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

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
    database.registrar_atividade(
        f'Talhão {nome} atualizado.'
    )
    return redirect(url_for('talhoes'))


#rotas do index
@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    producao = database.producao_total()

    custo = database.custo_operacional()

    talhoes = database.total_talhoes()

    area = database.area_total()

    atividades = database.buscar_atividades()

    dados_talhoes = database.dados_grafico_talhoes()
    nomes = []
    producoes = []
    for talhao in dados_talhoes:
        nomes.append(talhao[0])
        producoes.append(talhao[1])


    return render_template(
        'index.html',
        producao=producao,
        custo=custo,
        talhoes=talhoes,
        area=area,
        atividades=atividades,
        nomes=nomes,
        producoes=producoes
    )

#cadastro e login de usuários
@app.route('/cadastrar-usuario', methods=["GET","POST"])
def cadastrar_usuarios():


    if request.method == 'POST':

        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        senhaConfirm = request.form.get("senhaConfirm")

        if not nome or not email or not senha:
            return render_template(
                'cadastro.html',
                erro='Preencha todos os campos.')
        usuario = database.buscar_usuario_por_email(email)

        if usuario:
            return render_template(
                'login.html',
                erro="E-mail já cadastrado no sistema."
            )
        
        if (senha == senhaConfirm):
            senha_hash = generate_password_hash(senha)
            database.salvar_usuario(
                nome,
                email,
                senha_hash)
            
            database.registrar_atividade(
                f'Cadastro de usuário realizado')
            
            flash(f'Cadastro Realizado!')
            return redirect(url_for('login'))                
        else:
            return render_template(
            'cadastro.html',
            erro='As senhas precisam coincidir.',)

    return render_template(
        'cadastro.html',
    ) 



#rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = database.buscar_usuario_por_email(email)

        if not usuario:
            return render_template(
                'login.html',
                erro="Usuário ou senha incorretos."
            )
        if not check_password_hash(usuario[3],senha):
            return render_template(
                'login.html',
                erro='Usuário ou senha incorretos.')
        
        session["usuario_id"] = usuario[0]
        session["usuario_nome"] = usuario[1]
        

        return redirect(url_for('index'))
    return render_template('login.html')

#rota para sair de usuário
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))

# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)

