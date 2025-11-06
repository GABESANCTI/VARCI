# complex_ac_calculator.py

import cmath
import math

def Z_serie(impedancias):
    """
    Calcula a impedância equivalente para elementos conectados em SÉRIE.
    """
    return sum(impedancias)

def Z_paralelo(impedancias):
    """
    Calcula a impedância equivalente para elementos conectados em PARALELO.
    """
    if not impedancias: return complex(0, 0)
    
    # 1. Calcula a soma das admitâncias (inversos da impedância)
    soma_admitancias = sum([1 / z for z in impedancias])

    # Verifica se o denominador é quase zero (circuito aberto/ressonância)
    if abs(soma_admitancias) < 1e-9:
        # Retorna infinito para simular um circuito aberto (impedância muito alta)
        return complex(float('inf'), 0) 

    # 2. Impedância é o inverso da admitância total
    return 1 / soma_admitancias

def obter_Z_complexa_direta(R, XL, XC):
    """
    Cria a impedância complexa Z = R + j(XL - XC).
    """
    Z = complex(R, (XL - XC))
    return Z

def calcular_potencias(V_fonte, I_total, Z_total):
    """
    Calcula Potência Complexa (S), Ativa (P), Reativa (Q) e Fator de Potência (FP).
    """
    # S = V * I* (conjugado)
    S_total = V_fonte * I_total.conjugate()
    P_ativa = S_total.real
    Q_reativa = S_total.imag
    S_aparente = abs(S_total)
    
    # FP = cos(theta), onde theta é o ângulo de Z_total.
    fator_potencia = math.cos(cmath.phase(Z_total))
    
    return S_total, P_ativa, Q_reativa, S_aparente, fator_potencia