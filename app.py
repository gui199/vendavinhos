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

from flask import Flask
app = Flask(__name__)

#página inicial/home
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return 'Hello World!'
 
