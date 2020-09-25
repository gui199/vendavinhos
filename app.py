#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problema #1: Venda de Vinhos
Velasquez possui uma loja de vinhos e, ao longo dos anos, guardou dados de seus
clientes e um histórico de compras. Velasquez quer personalizar o atendimento e
contratou você para desenvolver um software que:
# 1 - Liste os clientes ordenados pelo maior valor total em compras.
# 2 - Mostre o cliente com maior compra única no último ano (2016).
Para criar esse software o neto do Velasquez (o Velasquinho) disponibilizou uma
API com cadastro de clientes
(​ http://www.mocky.io/v2/598b16291100004705515ec5​ ) e histórico de compras
(​ http://www.mocky.io/v2/598b16861100004905515ec7​ ).
@author: guilherme
"""

#importação dos módulos
import os
from flask import Flask, jsonify
import json
import pandas as pd
import requests

#definição de constantes, sites com json
#cadastro de clientes
site_cli = "http://www.mocky.io/v2/598b16291100004705515ec5"
#histórico de compras
site_hc =  "http://www.mocky.io/v2/598b16861100004905515ec7"

#funcao de requisicao de dados, 
#transforma a requisicao json em um dataframe(tabela) para facilitar a 
#manipulação de dados, foi usado a biblioteca pandas pois permite transformar
#json em dados tabular para melhor trabalhar e fazer busca e atualizações
def get_dados(site):
    #fazer a requisição do site
    r = requests.get(site, timeout=15)
    #transferir o json para uma variavel
    jason=r.json()
    #fechar a requisicção
    r.close()
    #transformar json em dataframe
    dframe_temp = pd.DataFrame(jason)
    return dframe_temp
 
# 1 - Liste os clientes ordenados pelo maior valor total em compras.
#função que retorna a atividade pedida
def get_lista_orden_cli():
    #variavel que armazena o dataframe dos clientes
    dframe_cli = get_dados(site_cli)
    #variavel que armazena o dataframe do histórico de compras dos clientes
    dframe_hc = get_dados(site_hc)
    # corrigir o cpf errado do cliente
    dframe_hc.loc[dframe_hc['cliente'] == '000.000.000.01', 'cliente'] = "0000.000.000.01"
    #lista vazia para armazenar os maiores valores total em compras
    novalista = []
    #loop para encontrar o maior valor para cada cliente
    for x in range(len(dframe_cli)):
        valor = round(dframe_hc[dframe_hc['cliente']== "0"+str(dframe_cli.iloc[x]["cpf"]).replace("-",".")]['valorTotal'].sum(), 2)
        novalista.append(valor)      
    #criação de uma nova coluna para cada cliente com o maior valor total em compras encontrado
    dframe_cli['valorTotal'] = novalista      
    #organizar a tabela em ordem descendente(maior para menor)
    dframe_cliente = dframe_cli.sort_values('valorTotal', ascending=False)  
    #retornar a tabela
    return dframe_cliente
    
# 2 - Mostre o cliente com maior compra única no último ano (2016).
#função que retorna a atividade pedida    
def get_maior_compra(ano):
    #variavel que armazena o dataframe dos clientes
    dframe_cli = get_dados(site_cli)
    #variavel que armazena o dataframe do histórico de compras dos clientes
    dframe_hc = get_dados(site_hc)
    # corrigir o cpf errado do cliente
    dframe_hc.loc[dframe_hc['cliente'] == '000.000.000.01', 'cliente'] = "0000.000.000.01"
    #transforma a variavel recebida em string
    ano = str(ano)
    #cria-se um novo dataframe com somente o ano desejado
    ddt = dframe_hc[dframe_hc["data"].str.contains(ano)]  
    #encontra-se o  cliente_maior_compra
    cmp=ddt[ddt['valorTotal']==ddt['valorTotal'].max()]['cliente'].array[0]
    #modfificar a string para o seu formato correspondente na outra tabela(cliente)
    cmp=cmp[::-1].replace(".","-",1)[::-1]    
    #buscar o perfi/dados do cliente desejado
    cliente_maior_compra = dframe_cli[dframe_cli['cpf'] == cmp[1:]]
    #retorna a linha/row com os dados do cliente
    return cliente_maior_compra
    


'''
Para criar uma api que retorne as api desejadas,
será utilizado o framework Flask.
'''
app = Flask(__name__)

#página inicial/home
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    #string contendo uma página html,
    #links para as api requisitadas
    return '''<h1>Home</h1>
    <p><a href="/api/v1/recursos/clientes/all" rel="gallery"> 1 - Liste os clientes ordenados pelo maior valor total em compras</a></p>
    <p><a href="/api/v1/recursos/clientes/maiorcompra/2016" rel="gallery"> 2 - Mostre o cliente com maior compra única no último ano (2016).</a></p>'''

#página de erro
@app.errorhandler(404)
def page_not_found(e):
    #string contendo uma página html,
    return "<h1>404</h1><p>Página não encontrada.</p>", 404

# 1 - Liste os clientes ordenados pelo maior valor total em compras.
@app.route('/api/v1/recursos/clientes/all', methods=['GET'])
def api_all():
    #variavel que armazena a lista/tabela com os clientes ordenados pelo maior valor total em compras
    cli_ordem = get_lista_orden_cli().to_json(orient="records")
    #trasnformação da var em formato json
    parsed = json.loads(cli_ordem)
    #envio da requisição
    return jsonify(parsed)

# 2 - Mostre o cliente com maior compra única no último ano (2016).
@app.route('/api/v1/recursos/clientes/maiorcompra/<name>', methods=['GET'])
def api_maior(name):
    #teste para verificar se a variavel passada é um valor numerico
    #e se o valor encontra-se entre 2014 e 2016
    #caso contrario retorna hello world
    if name.isnumeric() and int(name) >=2014 and int(name) <=2016:
        pass
    else:#        
        return {'hello': 'world'}
    #variavel que armazena a lista/tabela com o cliente com maior compra única no  ano especificado
    cli_maior = get_maior_compra(name).to_json(orient="records")
    parsed = json.loads(cli_maior)
    return jsonify(parsed)

#processo principal
if __name__ == "__main__":
    
    #iniciar aplicativo
    app.run(host='0.0.0.0',  threaded=True)
