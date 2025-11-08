#  Análise de Circuitos CA Monofásicos RLC

Este aplicativo foi desenvolvido para resolver e plotar **circuitos RLC (Resistor, Indutor e Capacitor)** em série, paralelo ou misto.  
O usuário insere os parâmetros e o sistema realiza automaticamente o **cálculo da impedância equivalente**, **fator de potência** e **plotagem de gráficos**.


---

## Funcionalidades

- Entrada de dados:
  - Resistência (**R**)
  - Indutância (**L**)
  - Capacitância (**C**)
  - Tipo de associação na carga (**Série / Paralelo**)

- Cálculos automáticos:
  - Impedância equivalente (**Z**)
  - Corrente total (**I**)
  - Fator de potência (**FP**)

- **Plotagem gráfica** das formas de onda de corrente e tensão.

- **Botão “Calcular tudo e plotar”** — realiza todos os cálculos e exibe o gráfico.

- **Botão “Limpar tudo” (vermelho)** — limpa todos os campos e resultados, permitindo uma nova análise sem reiniciar o programa.

---

## Interface

A interface foi criada com **Tkinter**, mantendo o layout simples e intuitivo:

- Campos de entrada  
- Botões:
  - **Calcular tudo e plotar**
  - **Limpar tudo**
- Resultados visíveis logo abaixo das entradas  
- Gráfico exibido em janela separada com `matplotlib`

---
##  Como Executar o Projeto

Baixe o projeto, via command line git ou download zip

### Na pasta do projeto crie um ambiente virtual:
```
python -m venv venv
venv\Scripts\activate
```
### Com o ambiente virtual execute o snippet abaixo:

```
pip install -r requirements.txt
```

### Após a instalação das dependencias é só rodar:
```
python main.py
```