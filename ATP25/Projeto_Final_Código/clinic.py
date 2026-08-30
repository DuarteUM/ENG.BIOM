import numpy as np
import json
import random

CHEGADA = "CHEGADA"
SAIDA = "SAIDA"

PULSEIRAS = {"vermelha": 0, "laranja": 1, "amarela": 2, "verde": 3}

def carregar_base_dados_pessoas(caminho_json):
    f = open(caminho_json, 'r', encoding='utf-8')
    dados = json.load(f)
    f.close()
    return dados

def gera_tempo_consulta(mean_service_time, dist, idade):
    media_ajustada = mean_service_time * 1.2 if idade > 65 else mean_service_time

    if dist == "exponential": 
        return np.random.exponential(media_ajustada)
    elif dist == "normal": 
        return max(1, np.random.normal(media_ajustada, media_ajustada / 3))
    
    return np.random.uniform(media_ajustada * 0.5, media_ajustada * 1.5)

def simula(num_medicos, taxa_chegada, tempo_medio_consulta, tempo_simulacao, dist_tempo_consulta, dados_pessoas):
    tempo_atual = 0
    queue_eventos = []
    
    while tempo_atual < tempo_simulacao:
        tempo_atual += np.random.exponential(60.0 / taxa_chegada)
        
        if tempo_atual < tempo_simulacao:
            pessoa = random.choice(dados_pessoas)
            
            hr = random.randint(40, 140)
            
            if hr < 50 or hr > 100:
                cor = "vermelha"
            else:
                testes = [random.choice([True, False]) for _ in range(3)]
                trues = sum(testes)
                
                if trues == 3:
                    cor = "vermelha"
                elif trues == 2:
                    cor = "laranja"
                elif trues == 1:
                    cor = "amarela"
                else:
                    cor = "verde"
            
            queue_eventos.append({
                'tempo': tempo_atual, 
                'tipo': CHEGADA, 
                'nome': pessoa['nome'],
                'idade': int(pessoa['idade']),
                'sexo': pessoa['sexo'].lower(),
                'cor': cor,
                'prioridade': PULSEIRAS[cor]
            })

    queue_eventos.sort(key=lambda x: x['tempo'])
    
    fila = []
    medicos = [[i, False, None, 0.0, 0.0] for i in range(num_medicos)]
    
    stats = {
        "atendidos": 0, 
        "espera": [], 
        "timeline_fila": [], 
        "timeline_tempo": [],
        "timeline_ocupacao": [], 
        "ocupacao_media": 0,
        "idades": [], 
        "sexos": [], 
        "cores_atendidas": [],
        "satisfacao_individual": [] 
    }
    chegadas = {}

    while queue_eventos:
        ev = queue_eventos.pop(0)
        t_evento, tipo, doente = ev['tempo'], ev['tipo'], ev
        
        if t_evento <= tempo_simulacao:
            stats["timeline_tempo"].append(t_evento)
            stats["timeline_fila"].append(len(fila))
            ocupados = sum(1 for m in medicos if m[1])
            stats["timeline_ocupacao"].append((ocupados / num_medicos) * 100)

        if tipo == CHEGADA:
            chegadas[doente['nome']] = t_evento
            medico_livre = next((m for m in medicos if not m[1]), None)
            
            if medico_livre:
                medico_livre[1], medico_livre[2], medico_livre[4] = True, doente['nome'], t_evento
                stats["espera"].append(0)
                stats["satisfacao_individual"].append(100) 
                stats["idades"].append(doente['idade'])
                stats["sexos"].append(doente['sexo'])
                stats["cores_atendidas"].append(doente['cor'])
                
                t_cons = gera_tempo_consulta(tempo_medio_consulta, dist_tempo_consulta, doente['idade'])
                queue_eventos.append({'tempo': t_evento + t_cons, 'tipo': SAIDA, 'nome': doente['nome']})
                queue_eventos.sort(key=lambda x: x['tempo'])
            else:
                fila.append(doente)
                fila.sort(key=lambda x: (x['prioridade'], x['tempo']))

        elif tipo == SAIDA:
            m = next((m for m in medicos if m[2] == doente['nome']), None)
            if m:
                fim_real = min(t_evento, tempo_simulacao)
                if fim_real > m[4]:
                    m[3] += (fim_real - m[4])
                
                m[1], m[2] = False, None
                stats["atendidos"] += 1
                
                if fila:
                    prox = fila.pop(0)
                    t_espera = max(0, t_evento - chegadas[prox['nome']])
                    
                    satisfacao = max(5, 100 - (max(0, t_espera - 10) * 1.5))
                    
                    m[1], m[2], m[4] = True, prox['nome'], t_evento
                    stats["espera"].append(t_espera)
                    stats["satisfacao_individual"].append(satisfacao)
                    stats["idades"].append(prox['idade'])
                    stats["sexos"].append(prox['sexo'])
                    stats["cores_atendidas"].append(prox['cor'])
                    
                    t_cons = gera_tempo_consulta(tempo_medio_consulta, dist_tempo_consulta, prox['idade'])
                    queue_eventos.append({'tempo': t_evento + t_cons, 'tipo': SAIDA, 'nome': prox['nome']})
                    queue_eventos.sort(key=lambda x: x['tempo'])

    total_trabalho = sum(m[3] for m in medicos)
    stats["ocupacao_media"] = min(100.0, (total_trabalho / (num_medicos * tempo_simulacao)) * 100)
    
    return stats, medicos