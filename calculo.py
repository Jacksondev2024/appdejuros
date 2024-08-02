from flask import Flask, request, jsonify
from scipy.optimize import fsolve
import os

app = Flask(__name__)

def calcular_taxa_juros(PMT, P, n, precisao=1e-6):
    def func(i):
        return PMT - (P * i) / (1 - (1 + i) ** -n)

    # Palpite inicial
    i_guess = 0.01

    # Resolvendo a função
    i_solution, = fsolve(func, i_guess)

    # Verificando a precisão da solução encontrada
    if abs(func(i_solution)) < precisao:
        return i_solution * 100
    else:
        return None

@app.route('/calcular_taxa', methods=['POST'])
def calcular_taxa():
    data = request.json
    PMT = data['PMT']
    P = data['P']
    n = data['n']
    taxa_juros_mensal = calcular_taxa_juros(PMT, P, n)
    return jsonify({'taxa_juros_mensal': taxa_juros_mensal})

if __name__ == '__main__':
    app.run()
