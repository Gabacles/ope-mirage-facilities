from requests import api


site_viacep = 'http://viacep.com.br/ws'


def busca_cep(cep):
    resultado = api.get(f"{site_viacep}/{cep}/json/")
    dic = resultado.json()
    return dic["logradouro"], dic["localidade"]
