from flask import Flask, request, jsonify
from scipy.optimize import fsolve
import numpy as np

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
    # Verificar o tipo de conteúdo da solicitação
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    
    try:
        # Obter e validar os dados JSON
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({'error': 'Formato de dados inválido'}), 400

        PMT = data.get('PMT')
        P = data.get('P')
        n = data.get('n')

        if PMT is None or P is None or n is None:
            return jsonify({'error': 'Dados insuficientes'}), 400

        try:
            PMT = float(PMT)
            P = float(P)
            n = int(n)
        except (ValueError, TypeError):
            return jsonify({'error': 'Dados inválidos'}), 400

        # Calcular a taxa de juros
        taxa_juros_mensal = calcular_taxa_juros(PMT, P, n)
        if taxa_juros_mensal is None:
            return jsonify({'error': 'Não foi possível calcular a taxa de juros'}), 500

        return jsonify({'taxa_juros_mensal': taxa_juros_mensal})

    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
