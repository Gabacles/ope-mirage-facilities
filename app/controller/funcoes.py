from app import db
from app.model.tables import User, Cliente, Cardapio, Pedido, ItensPedido


def busca_por_pedidos(nome=None, status=None, inicio=None, fim=None):
    if nome != '%' and nome and status and inicio and fim:
        print('ta em todos')
        busca = db.session.query(Pedido, Cliente).join(
            Cliente).filter(Cliente.nome.like(nome),
                            Pedido.status_pedido.like(status),
                            Pedido.data.between(inicio, fim))
        return busca
    elif status and inicio and fim:
        print('ta no status e data')
        busca = db.session.query(Pedido, Cliente).join(
            Cliente).filter(Pedido.status_pedido.like(status),
                            Pedido.data.between(inicio, fim))
        return busca
    elif status and inicio:
        print('ta no status e inicio')
        busca = db.session.query(Pedido, Cliente).join(
            Cliente).filter(Pedido.status_pedido.like(status),
                            Pedido.data.between(inicio, inicio))
        return busca
    elif nome != '%' and nome and status:
        print('ta no nome e status')
        busca = db.session.query(Pedido, Cliente).join(
            Cliente).filter(Cliente.nome.like(nome),
                            Pedido.status_pedido.like(status))
        return busca
    elif status:
        print('ta no status')
        busca = db.session.query(Pedido, Cliente).join(
            Cliente).filter(Pedido.status_pedido.like(status))
        return busca
    elif nome != '%' and nome:
        print('ta no nome')
        busca = db.session.query(Pedido, Cliente).join(
            Cliente).filter(Cliente.nome.like(nome))
        return busca
    elif inicio and fim:
        print('ta na data')
        busca = db.session.query(Pedido, Cliente).join(
            Cliente).filter(Pedido.data.between(inicio, fim))
        return busca
    else:
        return 0


def confere_negativo(numero):
    numero = numero.replace("-", "")
    return numero


def busca_cardapio(nome):
    busca = None
    if nome != '%':
        busca = Cardapio.query.filter(
            Cardapio.nome_produto.like(nome)).all()
    return busca


def total_vendido(busca):
    total = 0
    for itens, cardapio, pedido in busca:
        total += int(itens.quantidade)
    return total


def total_vendas_grafico(busca):
    itens_somados = {}
    itens_ordenados = {}
    cor = -1
    top = 1
    for itens, cardapio, pedido in busca:
        if not cardapio.nome_produto in itens_somados:
            itens_somados[cardapio.nome_produto] = [int(itens.quantidade), cor]
            cor -= 3
        else:
            itens_somados[cardapio.nome_produto][0] += int(itens.quantidade)
    for desc in sorted(itens_somados, key=itens_somados.get, reverse=True):
        itens_ordenados[desc] = itens_somados[desc]
        itens_ordenados[desc].append(top)
        top += 1
    return itens_ordenados


def total_vendas_mes(busca):
    vendas_ano = {"January": 0,
                  "Febuary": 0,
                  "March": 0,
                  "April": 0,
                  "May": 0,
                  "June": 0,
                  "July": 0,
                  "August": 0,
                  "September": 0,
                  "October": 0,
                  "November": 0,
                  "December": 0,
                  }
    for itens, pedido in busca:
        mes = pedido.data.strftime("%B")
        for mounth in vendas_ano:
            if mes == mounth:
                vendas_ano[mounth] += int(itens.quantidade)
    return vendas_ano


def total_pedidos_mes(busca):
    vendas_ano = {"January": 0,
                  "Febuary": 0,
                  "March": 0,
                  "April": 0,
                  "May": 0,
                  "June": 0,
                  "July": 0,
                  "August": 0,
                  "September": 0,
                  "October": 0,
                  "November": 0,
                  "December": 0,
                  }
    for pedido in busca:
        mes = pedido.data.strftime("%B")
        for mounth in vendas_ano:
            if mes == mounth and pedido.status_pedido == "atendido":
                vendas_ano[mounth] += 1
    return vendas_ano
