import json
import heapq #Ela gere uma "fila de prioridade" que ordena automaticamente as rotas em análise, fazendo com que o algoritmo teste sempre os caminhos mais fáceis e curtos primeiro, poupando memória e tempo de processamento.
import itertools #para criar um identificador numérico único para cada rota inserida na fila do Dijkstra, garantindo que o programa nunca se baralha ou bloqueia quando duas rotas têm exatamente o mesmo custo.

class EcoPathModel:
    def __init__(self):
        self.utilizadores = {}
        self.segmentos = []
        self.grafo = {}

    def ler_dados(self, ficheiro):
        with open(ficheiro, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.utilizadores = dados["users"]
            self.segmentos = dados["paths"]
            self._reconstruir_grafo()

    def _reconstruir_grafo(self):
        self.grafo = {}
        for p in self.segmentos:
            for u, v in [(p["origem"], p["destino"]), (p["destino"], p["origem"])]:
                if u not in self.grafo: self.grafo[u] = []
                seg_copy = p.copy()
                seg_copy["origem"], seg_copy["destino"] = u, v
                self.grafo[u].append(seg_copy)

    def adicionar_utilizador(self, nome, perfil, ficheiro='dados.json'):
        self.utilizadores[nome] = {"perfil": perfil, "pontos": 0}
        self._guardar_dados(ficheiro)

    def adicionar_pontos(self, nome, pontos, ficheiro='dados.json'):
        self.utilizadores[nome]["pontos"] += pontos
        self._guardar_dados(ficheiro)

    def _guardar_dados(self, ficheiro):
        dados = {"users": self.utilizadores, "paths": self.segmentos}
        with open(ficheiro, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def obter_locais(self):
        return sorted(list(self.grafo.keys()))

    def obter_segmento(self, u, v):
        for seg in self.grafo.get(u, []):
            if seg["destino"] == v: return seg
        return None

    def _calcular_peso(self, seg, perfil, modo="saude"):
        if modo == "distancia": return seg["distancia"]
        fator = 1.0 + (seg["ar"] * 0.1) + (seg["ruido"] * 0.05) - (seg["verde"] * 0.15)
        
        if perfil in ["Cadeira de Rodas", "Muletas", "Invisual"] and (seg["pavimento"] == "escadas" or seg["inclinacao"] > 6):
            fator += 100.0
        elif perfil in ["Cardiopata", "Idoso", "Lesão Temporária", "Grávida", "Doença Articular", "Fibromialgia", "Vertigens"] and (seg["pavimento"] == "escadas" or seg["inclinacao"] > 8):
            fator += 40.0
        elif perfil in ["Sedentário", "Obesidade", "Baixa Visão", "Défice Cognitivo", "Diabetes", "Surdez"] and (seg["pavimento"] == "escadas" or seg["inclinacao"] > 10):
            fator += 20.0
        elif perfil in ["Criança", "Asma", "Autismo"] and (seg["ar"] > 3 or seg["ruido"] > 3):
            fator += 15.0
            
        return max(seg["distancia"] * fator, 1.0)

    def calcular_rota(self, origem, destino, perfil, modo="saude", evitar_rota=None):
        arestas_evitar = set()
        if evitar_rota:
            for i in range(len(evitar_rota)-1):
                arestas_evitar.add((evitar_rota[i], evitar_rota[i+1]))
                arestas_evitar.add((evitar_rota[i+1], evitar_rota[i]))
                
        counter = itertools.count()
        pq = [(0, next(counter), origem, [])]
        visitados = set()
        
        while pq:
            custo, _, atual, caminho = heapq.heappop(pq)
            if atual in visitados: continue
            caminho = caminho + [atual]
            visitados.add(atual)
            
            if atual == destino: return caminho, custo
            
            if atual in self.grafo:
                for seg in self.grafo[atual]:
                    if seg["destino"] not in visitados:
                        peso = self._calcular_peso(seg, perfil, modo)
                        if evitar_rota and (atual, seg["destino"]) in arestas_evitar:
                            peso += 100000.0 
                        heapq.heappush(pq, (custo + peso, next(counter), seg["destino"], caminho))
        return None, 0