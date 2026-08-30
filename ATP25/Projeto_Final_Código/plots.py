import matplotlib.pyplot as plt
import numpy as np

def mostrar_grafico_fila(stats):
    plt.figure("Evolução da Fila", figsize=(10, 5))
    plt.step(stats["timeline_tempo"], stats["timeline_fila"], where='post', color='blue', linewidth=1.5)
    plt.fill_between(stats["timeline_tempo"], stats["timeline_fila"], step="post", alpha=0.3)
    plt.title("Evolução do Tamanho da Fila de Espera")
    plt.xlabel("Tempo de Simulação (minutos)")
    plt.ylabel("Número de Doentes na Fila")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def mostrar_grafico_ocupacao(stats):
    plt.figure("Ocupação dos Médicos", figsize=(10, 5))
    plt.step(stats["timeline_tempo"], stats["timeline_ocupacao"], where='post', color='green', linewidth=1.5)
    plt.fill_between(stats["timeline_tempo"], stats["timeline_ocupacao"], step="post", alpha=0.2, color='green')
    plt.title("Evolução da Taxa de Ocupação dos Médicos")
    plt.xlabel("Tempo de Simulação (minutos)")
    plt.ylabel("Ocupação (%)")
    plt.ylim(0, 110)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def mostrar_grafico_correlacao(eixo_x, eixo_y):
    plt.figure("Correlação Taxa/Fila", figsize=(10, 5))
    plt.plot(eixo_x, eixo_y, marker='s', color='red', linestyle='-', linewidth=2)
    plt.title("Relação: Taxa de Chegada vs Tamanho Médio da Fila")
    plt.xlabel("Taxa de Chegada (doentes/hora)")
    plt.ylabel("Tamanho Médio da Fila")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def mostrar_grafico_faixas_etarias(idades):
    bins = [18, 30, 45, 60, 75, 120]
    labels = ['18-30', '31-45', '46-60', '61-75', '+75']
    counts = np.histogram(idades, bins=bins)[0]
    
    plt.figure("Faixas Etárias", figsize=(10, 5))
    plt.barh(labels, counts, color='teal')
    plt.title("Distribuição Etária Detalhada dos Atendidos")
    plt.xlabel("Número de Doentes")
    plt.ylabel("Faixas Etárias (Anos)")
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.show()

def mostrar_grafico_manchester(cores_atendidas):
    labels = ['Vermelha', 'Laranja', 'Amarela', 'Verde']
    counts = [
        cores_atendidas.count('vermelha'), 
        cores_atendidas.count('laranja'), 
        cores_atendidas.count('amarela'), 
        cores_atendidas.count('verde')
    ]
    colors = ['#ff0000', '#ff8c00', '#ffff00', '#00ff00']
    explode = (0.1, 0, 0, 0) if cores_atendidas.count('vermelha') > 0 else (0, 0, 0, 0)
    
    plt.figure("Triagem de Manchester", figsize=(8, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, 
            startangle=140, shadow=True, explode=explode)
    plt.title("Distribuição de Prioridade por Cores")
    plt.show()