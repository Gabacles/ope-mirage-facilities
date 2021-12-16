from app import app, db
from flask import render_template, request, redirect, url_for, flash, session
from app.model.tables import User, Cliente, Cardapio, Pedido, ItensPedido
from .funcoes import busca_cardapio, busca_por_pedidos, confere_negativo, total_pedidos_mes, total_vendas_grafico, total_vendas_mes, total_vendido


count = 1


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        return
    return render_template('contato.html')


@app.route('/dashboard')
def dashboard():
    if not 'usuario' in session:
        return redirect('/')
    else:
        pedido = db.session.query(Pedido, Cliente).join(
            Cliente).filter(Pedido.status_pedido.like('aberto'))
        #busca = db.session.query(ItensPedido, Pedido).join(
            #Pedido).all()
        busca_pedidos = Pedido.query.all()
        vendas_mensais = total_pedidos_mes(busca_pedidos)
        return render_template('dashboard.html',
                               vendas_mensais=vendas_mensais,
                               pedido=pedido
                               )


@app.route('/grafico')
def grafico():
    if not 'usuario' in session:
        return redirect('/')
    else:
        busca = db.session.query(ItensPedido, Cardapio, Pedido).select_from(
            ItensPedido).join(Cardapio).join(Pedido).all()
        total_vendas = total_vendas_grafico(busca)
        for itens in total_vendas:
            print(itens)
        return render_template('graficos.html',
                               busca=busca,
                               total_vendas=total_vendas
                               )


@app.route("/")
def home():
    usuarios = User.query.all()
    return render_template('index.html', usuarios=usuarios)

# CRUD Cliente


@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        count = 1
        nome_encontrado = None
        client = Cliente.query.all()
        if request.method == 'POST':
            nome_procurado = request.form['busca']
            busca = "{}%".format(nome_procurado)
            if len(busca) > 1:
                nome_encontrado = Cliente.query.filter(
                    Cliente.nome.like(busca)).all()
            if nome_encontrado:
                client = nome_encontrado
                return render_template('clientes.html',
                                       client=client,
                                       nome_encontrado=nome_encontrado)
        return render_template('clientes.html', client=client)


@app.route("/add-cliente", methods=['GET', 'POST'])
def addCliente():
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        count = 1
        if request.method == 'POST':
            cliente = Cliente(request.form['nome'],
                              request.form['cpf'],
                              request.form['email'],
                              request.form['telefone'],
                              request.form['cep'],
                              request.form['endereco'],
                              request.form['cidade'])
            db.session.add(cliente)
            db.session.commit()
            return redirect(url_for('clientes'))
        return render_template('addcliente.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        count = 1
        cliente = Cliente.query.get(id)
        if request.method == 'POST':
            cliente.nome = request.form['nome']
            cliente.cpf = request.form['cpf']
            cliente.email = request.form['email']
            cliente.telefone = request.form['telefone']
            cliente.cep = request.form['cep']
            cliente.logradouro = request.form['endereco']
            cliente.cidade = request.form['cidade']
            db.session.commit()
            return redirect('/clientes')
        return render_template('editar-cliente.html', cliente=cliente)


@app.route('/deletar/<int:id>')
def deletar(id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        cliente = Cliente.query.get(id)
        db.session.delete(cliente)
        db.session.commit()
        return redirect('/clientes')

# CRUD Cardápio


@app.route("/cardapio", methods=['GET', 'POST'])
def cardapio():
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        count = 1
        produto_encontrado = None
        produtos = Cardapio.query.all()
        if request.method == 'POST':
            produto_procurado = request.form['busca']
            nome_produto = "{}%".format(produto_procurado)
            produto_encontrado = busca_cardapio(nome_produto)
            if produto_encontrado:
                produtos = produto_encontrado
                return render_template('cardapio.html',
                                       produtos=produtos,
                                       produto_encontrado=produto_encontrado)
        return render_template('cardapio.html', produtos=produtos)


@app.route("/historico/<int:id_produto>")
def historico_do_produto(id_produto):
    busca = db.session.query(ItensPedido, Cardapio, Pedido).select_from(
        ItensPedido).join(Cardapio).join(Pedido).filter(
        ItensPedido.id_produto.like(id_produto)).all()
    total_vendas = total_vendido(busca)
    return render_template('historico-cardapio.html',
                           busca=busca,
                           total_vendas=total_vendas
                           )


@app.route("/add-cardapio", methods=['GET', 'POST'])
def addProduto():
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        count = 1
        if request.method == 'POST':
            quantidade = confere_negativo(request.form['quantidade'])
            cardapio_produto = Cardapio(request.form['nome-produto'],
                                        quantidade,)
            db.session.add(cardapio_produto)
            db.session.commit()
            return redirect(url_for('cardapio'))
        return render_template('addcardapio.html')


@ app.route('/editar-cardapio/<int:id>', methods=['GET', 'POST'])
def editarProduto(id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        count = 1
        produto = Cardapio.query.get(id)
        if request.method == 'POST':
            produto.nome_produto = request.form['nome-produto']
            produto.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect('/cardapio')
        return render_template('editar-cardapio.html', produto=produto)


@ app.route('/deletar-produto/<int:id>')
def deletarProduto(id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        produto = Cardapio.query.get(id)
        db.session.delete(produto)
        db.session.commit()
        return redirect('/cardapio')


# CRUD Pedidos


@ app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        count = 1
        pedido = db.session.query(Pedido, Cliente).join(
            Cliente).filter(Pedido.status_pedido.like('aberto'))
        nome = None
        if request.method == 'POST':
            tag = request.form['busca']
            try:
                status_pedido = request.form['status']
            except KeyError:
                status_pedido = 0
            busca_por_data_inicio = request.form['date-inicio']
            busca_por_data_fim = request.form['date-fim']
            nome_cliente = "{}%".format(tag)
            nome = busca_por_pedidos(
                nome_cliente, status_pedido,
                busca_por_data_inicio, busca_por_data_fim)
            if nome:
                pedido = nome
                return render_template('pedidos.html',
                                       pedido=pedido,
                                       nome=nome
                                       )
        return render_template('pedidos.html', pedido=pedido)


@app.route("/addpedido/<int:id>", methods=['GET', 'POST'])
def addPedido(id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        cliente = Cliente.query.get(id)
        cardapio = Cardapio.query.all()
        if request.method == 'POST':
            pedido = Pedido(id)
            db.session.add(pedido)
            db.session.commit()
            for i in range(count):
                quantidade = request.form[f'quantidade{i}']
                qtd = confere_negativo(quantidade)
                produtos = ItensPedido(
                    pedido.id_pedido, f"{request.form[f'id-produto{i}']}",
                    qtd)
                db.session.add(produtos)
                db.session.commit()
            return redirect('/pedidos')
        return render_template('addpedido.html',
                               cliente=cliente,
                               count=count,
                               cardapio=cardapio)


@ app.route('/editar-pedido/<int:id>', methods=['GET', 'POST'])
def editarPedido(id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        count = 1
        quantidades = []
        contador = 0
        print(contador)
        pedido = db.session.query(Cliente, Pedido, ItensPedido).select_from(
            Cliente).join(Pedido).join(ItensPedido).filter(
            Pedido.id_pedido.like(id)).all()
        nome_cliente = pedido[0][0].nome
        produtos_quantidade = {}
        produto = Pedido.query.get(id)
        for cliente, pedido, itens in pedido:
            nomeproduto = Cardapio.query.get(int(itens.id_produto))
            produtos_quantidade[itens.id_itens_pedi] = [
                itens.id_produto, nomeproduto.nome_produto, itens.quantidade]
        if request.method == 'POST':
            pedido2 = db.session.query(Cliente, Pedido, ItensPedido).select_from(
                Cliente).join(Pedido).join(ItensPedido).filter(
                Pedido.id_pedido.like(id)).all()
            produto.status_pedido = request.form['status']
            for p in produtos_quantidade:
                quantidades.append(request.form[f'quantidade{p}'])
            for cliente, pedi, itens in pedido2:
                itens.quantidade = quantidades[contador]
                contador += 1
            db.session.commit()
            return redirect('/pedidos')
        return render_template('editar-pedido.html',
                               produto=produto,
                               pedido=pedido,
                               nome_cliente=nome_cliente,
                               produtos_quantidade=produtos_quantidade
                               )


@app.route('/atualizar-status/<int:id>/<status>')
def atualizarStatus(id, status):
    pedido = Pedido.query.get(id)
    print(id)
    pedido.status_pedido = status
    db.session.commit()
    return redirect('/pedidos')


@app.route('/deletar-item-pedido/<int:id_item>/<int:id_prod>/<int:id>')
def deletarItemPedido(id_item, id_prod, id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        quantidade_itens = 0
        busca_itens = db.session.query(ItensPedido).filter(
            ItensPedido.id_pedido.like(id))
        for qtd in busca_itens:
            quantidade_itens += 1
        print(quantidade_itens)
        if quantidade_itens > 1:
            busca_item_deletado = db.session.query(ItensPedido).filter(
                ItensPedido.id_itens_pedi.like(id_item),
                ItensPedido.id_produto.like(id_prod))
            for item_deletado in busca_item_deletado:
                db.session.delete(item_deletado)
                db.session.commit()
        else:
            flash("Não é possível excluir este produto!")
        return redirect(f'/editar-pedido/{id}')


@ app.route('/deletar-pedido/<int:id>')
def deletarPedido(id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        pedido_deletado = db.session.query(Pedido, ItensPedido).select_from(
            Pedido).join(ItensPedido).filter(Pedido.id_pedido.like(id)).all()
        db.session.delete(pedido_deletado[0][0])
        for pedido, itens in pedido_deletado:
            produto = ItensPedido.query.get(itens.id_itens_pedi)
            db.session.delete(produto)
        db.session.commit()
        return redirect('/pedidos')


@ app.route('/aumentar/<int:id>')
def aumentar(id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        count += 1
        return redirect(f'/addpedido/{id}')


@ app.route('/diminuir/<int:id>')
def diminuir(id):
    if not 'usuario' in session:
        return redirect('/')
    else:
        global count
        if count > 1:
            count -= 1
        return redirect(f'/addpedido/{id}')


@ app.route('/autenticar', methods=['POST'])
def autenticar():
    form = request.form
    usuario = form.get('usuario')
    senha = form.get('senha')
    users = User.query.all()
    for user in users:
        if user.username == usuario and user.password == senha:
            session['usuario'] = user.username
            return redirect(url_for('dashboard'))
    else:
        flash('Usuário ou senha inválidos')
        return redirect(url_for('home'))


@ app.route('/sair')
def sair():
    session.clear()
    return redirect('/')
