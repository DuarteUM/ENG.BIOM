import tkinter as tk #cria a janela com menus e programas
from tkinter import messagebox #serve para mostrar os avisos pop-up de erro e de ponto ganhados po rexemplo
import threading #serve para o terminal consola e a interface funcionem ao mesmo tempo
import shlex #serve para ler os nomes na consola com espaços como um só elemento ex: "Adelaide Costa"
import os #serve para fechar o programa, e conferir se existem os ficheiro s.txt no computador
import sys #é oque permite interagir com o sistema para controalr internamente o programa
from model import EcoPathModel #aqui estamos a importar o model que é usado para calcular rotas e pontos do utilizador
from view import EcoPathView #aqui estamos a importar o view para desenhar os mapas de braga e os menus

class EcoPathController:
    def __init__(self):
        self.model = EcoPathModel() #cria ligaçao com o model para criar rotas e pontos
        self.root = tk.Tk() #cria janela em branco onde o programa vai rodar
        self.view = EcoPathView(self.root, self) #cria a parte visual botões e mapas na janela principal
        self.usuario_atual = None #guarda o nome do utilizador que começa vazio
        self.rotas_temp = {} #guarda temporariamente as rotas calculadas para o utilizador poder escolher
        self.historico_sessao = {} #guarda registo dos caminhos feitos e pontos ganho na sessão
        self.iniciar() #chama a funçao que carrega os dados do json
        
        threading.Thread(target=self.iniciar_cli, daemon=True).start() #ativa o terminal de texto em segundo plano vai funcionar ao mesmo tempo que a janela

    def iniciar(self):
        self.model.ler_dados('dados.json') #carrega todas as ruas e caminho do json assim como utilizadores
        self.view.preencher_login_dropdown(self.model.utilizadores) #coloca os utilizadores pendentes para serem escolhidos

    def iniciar_cli(self):
        print("\n" + "="*60) # efeito estético para separar a consola a ser escrita da consola do programa
        print("🌍 BEM-VINDO AO TERMINAL ECOPATH (CLI) 🌍")
        print("Comandos suportados (use aspas para nomes com espaços):")
        print(" - ins_utilizador \"<nome>\" \"<perfil>\"")
        print(" - escolher_utilizador \"<nome>\"")
        print(" - ins_percurso \"<origem>\" \"<destino>\"")
        print(" - recomendar \"<origem>\" \"<destino>\"")
        print(" - escolher_caminho <1 ou 2>")
        print(" - list percursos")
        print(" - ver \"<percurso>\"")
        print(" - gravar \"<ficheiro.txt>\"")
        print(" - ler \"<ficheiro.txt>\"")
        print(" - sair")
        print("="*60 + "\n") #efeito estético para separar a consola a ser escrita da consola do programa
        
        while True:
            try:
                linha = input("\nEcoPath> ").strip() #mostra o texto na consola e guarda o texto que o utilizador submeteu no terminal
                if not linha: continue #se o tuilizador não escrever nada e clicar no enter volta ao inicio
                
                try:
                    args = shlex.split(linha) #divide a frase escrita em palavras mas os nomes entre aspas deixa-os como apenas 1
                except ValueError: #deteta se o utilizador cometeu algum erro ao esquecer-se das aspas
                    print("❌ Erro de sintaxe (verifique se fechou as aspas).")
                    continue #salta o codigo volta ao inicio a pedir um novo comando
                    
                cmd = args[0].lower() #pega na primeira palavras digitada e transforma todas as letras em minusculas
                
                if cmd == "sair": #verifica se o utilizador quer fechar o programa
                    print("A encerrar o EcoPath...") 
                    self.root.after(0, self.root.destroy) #diz a janela no tkinker para se fechar o mais rapido possível
                    os._exit(0) #força encerramento imediato de todos os processos
                    
                elif cmd == "ins_utilizador": #verificamos se o codigo digitado é o de adicionar utilizador
                    if len(args) < 3: #verifica se o utilizador escreveu menos de 3 palavras comando nome e perfil
                        print("Uso: ins_utilizador \"<nome>\" \"<perfil>\"") #mostra o formaod correto
                        continue #volta ao inicio
                    nome, perfil = args[1], args[2] #guarda a segunda palavra na variavel nome e a terceira na varivel perfil
                    self.model.adicionar_utilizador(nome, perfil, 'dados.json') #diz ao model para guardar o novo utilizador 
                    self.root.after(0, lambda: self.view.preencher_login_dropdown(self.model.utilizadores)) #interface atualiza novo nome
                    print(f"✅ Utilizador '{nome}' registado com a condição '{perfil}'.")

                elif cmd == "escolher_utilizador": #verifica se decidimos escolher utilizador
                    if len(args) < 2: #verifica se o utilizador se enganou a submeter o comando
                        print("Uso: escolher_utilizador \"<nome>\"") #mostra a forma correta
                        continue #volta ao inicio
                    nome = args[1] #guarda a variavel nome como o nome citado
                    if nome in self.model.utilizadores: #verifica se o nome esta presente na lista
                        self.usuario_atual = nome #define essa pessoa como o utilizador ativo a mexer no programa
                        if nome not in self.historico_sessao: #verifica se este utilizador ja tinha mexido na aplicação ou se é a 1ºvez
                            self.historico_sessao[nome] = {"perfil": self.model.utilizadores[nome]["perfil"], "trajetos": [], "pontos_sessao": 0} #cria uma ficha em branco para guardar os dados do que ele fizer
                        print(f"✅ O utilizador '{nome}' está agora selecionado para explorar rotas.") #confirma na consola
                    else:
                        print("❌ Utilizador não encontrado. Crie primeiro com 'ins_utilizador'.") #diz que nao foi encontrado caso nao esteja no json
                        
                elif cmd == "ins_percurso": #ver se o comando utilizado serve para procurar caminho
                    if len(args) < 3: #vê se escreveste a partida e a chegada
                        print("Uso: ins_percurso \"<origem>\" \"<destino>\"") #mostra como se deve escrever
                        continue
                    self.mostrar_opcoes_percurso(args[1], args[2]) #chama a funçao que calcula e mostra as rostas de saúde e de distancia

                elif cmd == "recomendar": #ve se estamos a pedir este comando recomendar
                    if len(args) < 3: #ve se estamos a escrever o numero de plavras suficiente
                        print("Uso: recomendar \"<origem>\" \"<destino>\"") #mostra a forma como se deve escrever
                        continue
                    self.mostrar_recomendacao(args[1], args[2]) #ativa a funçao que gera a melhor rota para a condiçao da pessoa
                    
                elif cmd == "escolher_caminho": #pergunta se queremos escolher o caminho 
                    if len(args) < 2: #ve se estamos a escrever corretamente
                        print("Uso: escolher_caminho <1 ou 2>") #mostra a forma correta de designar
                        continue
                    if not self.usuario_atual: #se ainda nao tivermos escolhido um usuário
                        print("❌ Selecione um utilizador primeiro.")
                        continue
                        
                    idx = args[1] #guarda o numero da rota esoclhido
                    if idx in self.rotas_temp: #Verifica se esse número corresponde a uma rota que foi calculada e está guardada na memória temporária.
                        dados = self.rotas_temp[idx] #copia infos dessa rota para a variavel dados
                        pts = dados['pontos'] #retira dos valores dos pontos daquela rota e guarda na memoria temporaria
                        ruas = dados['trajeto'] #retira dos valores das ruas daquela rota e guarda na memoria temporaria
                        
                        self.model.adicionar_pontos(self.usuario_atual, pts) #diz ao model para somar os pontos ao utilizador no json
                        self.historico_sessao[self.usuario_atual]["trajetos"].append(ruas) #adiciona o nome das ruas percorridas a lista de trajetos percorridos hj
                        self.historico_sessao[self.usuario_atual]["pontos_sessao"] += pts #soma o spontos ao contador da sessão atual
                        
                        print(f"✅ Excelente! Caminho concluído. Ganhou {pts} pontos!")
                        print(f"🏆 Total atual de {self.usuario_atual}: {self.model.utilizadores[self.usuario_atual]['pontos']} pontos.")
                    else:
                        print("❌ Opção inválida. Calcule uma rota com 'ins_percurso' primeiro e escolha [1] ou [2].")
                        
                elif cmd == "list" and len(args) > 1 and args[1].lower() == "percursos":
                    print("--- LISTA DE PERCURSOS DO MAPA ---")
                    for p in self.model.segmentos: #serve para listar dos caminhos todos no mapa
                        print(f"- {p['nome']} ({p['origem']} <-> {p['destino']})")
                        
                elif cmd == "ver":
                    if len(args) < 2:
                        print("Uso: ver \"<percurso>\"")
                        continue
                    nome_perc = args[1] #guarda o nome da rua a ser inspecionada
                    encontrado = next((p for p in self.model.segmentos if p['nome'].lower() == nome_perc.lower()), None) #procura de a rua existe na base de dados
                    if encontrado:
                        print(f"--- INFO DO PERCURSO: {encontrado['nome']} ---")
                        for k, v in encontrado.items(): print(f"  {k.capitalize()}: {v}")
                        print("➡️ A apresentar o segmento isolado no mapa gráfico a amarelo...")
                        mock_rota = {"Percurso Isolado": {"nodos": [encontrado["origem"], encontrado["destino"]], "cor_hex": "#f1c40f"}} #pinta a rua de amarelo no mapa
                        self.root.after(0, lambda m=mock_rota: self.view.desenhar_mapa(self.model.segmentos, m)) #diz a interface para abrir o mapa
                    else:
                        print("❌ Percurso não encontrado.")
                        
                elif cmd == "gravar":
                    if len(args) < 2:
                        print("Uso: gravar \"<ficheiro.txt>\"")
                        continue
                    ficheiro = args[1] #guarda no me ficheiro escolhido
                    if not ficheiro.endswith(".txt"): ficheiro += ".txt" #adiciona o .txt por nos caos nos tenhamos esquecido
                    
                    try: #este todo serve para gravar os dados da sessão
                        with open(ficheiro, "w", encoding="utf-8") as f:
                            f.write("=== RELATÓRIO DA SESSÃO ATUAL ECOPATH ===\n\n")
                            if not self.historico_sessao:
                                f.write("Nenhuma atividade foi registada nesta sessão de consola.\n")
                            else:
                                for u, d in self.historico_sessao.items():
                                    f.write(f"👤 Utilizador Ativo: {u} (Perfil: {d['perfil']})\n")
                                    f.write(f"   ⭐ Pontos ganhos nesta sessão: {d['pontos_sessao']} pts\n")
                                    f.write(f"   🛣️ Trajetos percorridos:\n")
                                    if not d['trajetos']:
                                        f.write("      (Nenhum caminho concluído)\n")
                                    else:
                                        for t in d['trajetos']:
                                            f.write(f"      - {t}\n")
                                    f.write("\n")
                        print(f"✅ Histórico das atividades desta sessão gravado em '{ficheiro}'.")
                    except Exception as e:
                        print(f"❌ Erro ao gravar o ficheiro: {e}")
                        
                elif cmd == "ler": # este todo serve para abrir o ficheiro e fazer print dos dados
                    if len(args) < 2:
                        print("Uso: ler \"<ficheiro.txt>\"")
                        continue
                    ficheiro = args[1]
                    if not ficheiro.endswith(".txt"): ficheiro += ".txt"
                    if not os.path.exists(ficheiro):
                        print(f"❌ O ficheiro '{ficheiro}' não foi encontrado.")
                        continue
                    with open(ficheiro, "r", encoding="utf-8") as f:
                        print("\n" + "="*50 + f"\n📄 A LER CONTEÚDO DE: {ficheiro}\n" + "="*50)
                        print(f.read())
                        print("="*50)
                else:
                    print("❌ Comando não reconhecido.")
            except Exception as e:
                print(f"❌ Erro inesperado na consola: {e}")

    def mostrar_opcoes_percurso(self, ori, dest): #funçao que cria calcula e mostra os percursos entre a origem e o destino
        if not self.usuario_atual:
            print("❌ ATENÇÃO: Use primeiro 'escolher_utilizador \"<nome>\"' para sabermos quem vai fazer o caminho.")
            return
            
        perfil = self.model.utilizadores[self.usuario_atual]["perfil"] #perfil
        r1_c, _ = self.model.calcular_rota(ori, dest, perfil, "saude") #pede ao modelo que calcule rota baseada na saude
        r2_c, _ = self.model.calcular_rota(ori, dest, perfil, "distancia") #pede ao modelo para calcular uma rota mais curta em metros
        
        if r1_c == r2_c: #verifica se os caminhos saude e distanca deram iguais
            r_alt, _ = self.model.calcular_rota(ori, dest, perfil, "distancia", evitar_rota=r1_c) #se estes derem iguais o modelo cria um alternativo
            if r_alt and r_alt != r1_c: r2_c = r_alt #define esta rota como segunda rota
            
        print(f"\n🛣️ OPÇÕES PARA {self.usuario_atual.upper()} ENTRE {ori} E {dest}:")
        self.rotas_temp = {} #limpa o dicionário de rotas antigas e prepara-o para novas
        
        if r1_c: #verifica se é possivel calcular uma rota valida para saúde
            d1 = self.analisar_rota(r1_c, perfil) #analisa o trejeto saude e extrai estatisticas como esforço, tempo pontos...
            self.rotas_temp["1"] = d1 #guarda a rota 1 na chave 1
            ruas_1 = [self.model.obter_segmento(r1_c[i], r1_c[i+1])['nome'] for i in range(len(r1_c)-1)]
            print(f" [1] Opção Saúde: {' -> '.join(ruas_1)} | Recompensa: {d1['pontos']} pts")
            
        if r2_c and r2_c != r1_c: 
            d2 = self.analisar_rota(r2_c, perfil)
            self.rotas_temp["2"] = d2
            ruas_2 = [self.model.obter_segmento(r2_c[i], r2_c[i+1])['nome'] for i in range(len(r2_c)-1)]
            print(f" [2] Opção Distância: {' -> '.join(ruas_2)} | Recompensa: {d2['pontos']} pts")
            
        if not self.rotas_temp:
            print("❌ Não foram encontrados caminhos compatíveis.")
        else:
            print("\n👉 Use o comando 'escolher_caminho <1 ou 2>' para confirmar e ganhar pontos.")

    def mostrar_recomendacao(self, ori, dest):
        if not self.usuario_atual:
            print("❌ ATENÇÃO: Use primeiro 'escolher_utilizador \"<nome>\"' para sabermos quem vai fazer o caminho.")
            return
            
        perfil = self.model.utilizadores[self.usuario_atual]["perfil"]
        r1_c, _ = self.model.calcular_rota(ori, dest, perfil, "saude")
        
        if not r1_c:
            print("❌ Não foi possível encontrar uma rota compatível para este destino.")
            return
            
        d1 = self.analisar_rota(r1_c, perfil)
        print(f"\n🌟 CAMINHO FAVORITO (RECOMENDADO) PARA: {self.usuario_atual.upper()} (Perfil: {perfil}) 🌟")
        print(self.formatar_relatorio(d1))

    def processar_login(self, nome, password):
        if not nome:
            messagebox.showerror("Erro", "Selecione um utilizador da lista.")
            return
        if password == "2026":
            self.usuario_atual = nome
            locais = self.model.obter_locais()
            self.view.mostrar_ecran_principal(locais)
        else:
            messagebox.showerror("Erro", "Password incorreta! Tente novamente.")

    def processar_registo(self, nome, handicap):
        if not nome.strip():
            messagebox.showerror("Erro", "O nome não pode estar vazio.")
            return
        if not handicap:
            messagebox.showerror("Erro", "Selecione uma opção de condição.")
            return
        
        self.model.adicionar_utilizador(nome.strip(), handicap, 'dados.json')
        self.view.preencher_login_dropdown(self.model.utilizadores)
        messagebox.showinfo("Sucesso", f"{nome} registado com sucesso! Já pode entrar no separador ao lado.")

    def abrir_mapa(self):
        self.view.desenhar_mapa(self.model.segmentos, self.rotas_temp)

    def analisar_rota(self, rota, perfil):
        dist, inc_max, soma_inc, verde_tot = 0, 0, 0, 0
        ar_max, ruido_max = 0, 0
        detalhe = []
        for i in range(len(rota)-1):
            seg = self.model.obter_segmento(rota[i], rota[i+1])
            dist += seg["distancia"]
            inc_max = max(inc_max, seg["inclinacao"])
            soma_inc += seg["inclinacao"]
            verde_tot += seg["verde"]
            ar_max = max(ar_max, seg["ar"])
            ruido_max = max(ruido_max, seg["ruido"])
            detalhe.append(f"  • {rota[i]} -> {rota[i+1]} ({seg['nome']}): {seg['distancia']}m, Inc: {seg['inclinacao']}%")
        
        if perfil == "Jovem Saudável": v = 1.4
        elif perfil in ["Sedentário", "Criança", "Autismo"]: v = 1.2
        elif perfil in ["Grávida", "Asma", "Obesidade"]: v = 1.0
        else: v = 0.8 
        
        tempo = (dist / v) / 60
        pontos_calculados = int((dist / 10) + (inc_max * 10))
        
        status = "✅ Percurso adequado para mobilidade ativa"
        if perfil in ["Cadeira de Rodas", "Muletas", "Invisual"]:
            if inc_max > 6 or dist > 1500: status = "⚠️ PERIGO: Percurso inacessível/perigoso. Recomendado CARRO"
        elif perfil in ["Cardiopata", "Idoso", "Lesão Temporária", "Grávida", "Doença Articular", "Fibromialgia", "Vertigens"]:
            if inc_max > 8 or dist > 2500: status = "⚠️ PERIGO: Risco de esforço físico excessivo. Recomendado CARRO"
        elif perfil in ["Asma", "Criança", "Autismo"]:
            if ar_max > 3 or ruido_max > 3 or dist > 3000: status = "⚠️ AVISO: Exposição a ambiente ruidoso/poluído/longo."
        elif perfil in ["Sedentário", "Obesidade", "Baixa Visão", "Défice Cognitivo", "Diabetes", "Surdez"]:
            if inc_max > 10 or dist > 4000: status = "⚠️ AVISO: Percurso extenuante ou complexo. Faça pausas."
        else:
            if inc_max > 15 or dist > 6000: status = "⚠️ AVISO: Percurso longo ou inclinado."

        ruas_bonitas = [self.model.obter_segmento(rota[i], rota[i+1])['nome'] for i in range(len(rota)-1)]
        return {
            "dist": dist/1000, "tempo": tempo, "inc": soma_inc/(len(rota)-1), "inc_max": inc_max,
            "esforco": "Baixo" if inc_max <= 4 else ("Médio" if inc_max <= 8 else "Alto"),
            "status": status, "verde": verde_tot/(len(rota)-1), "detalhe": "\n".join(detalhe), 
            "trajeto": " -> ".join(ruas_bonitas), "pontos": pontos_calculados, "nodos": rota 
        }

    def processar_rota(self):
        ori, dest = self.view.cb_origem.get(), self.view.cb_destino.get()
        if ori == dest: self.view.atualizar_resultado("⚠️ Origem e destino iguais."); return
        perfil = self.model.utilizadores[self.usuario_atual]["perfil"]
        
        r1_c, _ = self.model.calcular_rota(ori, dest, perfil, "saude")
        d1 = self.analisar_rota(r1_c, perfil)
        
        r2_c, _ = self.model.calcular_rota(ori, dest, perfil, "distancia")
        
        if r1_c == r2_c:
            r_alt, _ = self.model.calcular_rota(ori, dest, perfil, "distancia", evitar_rota=r1_c)
            if r_alt and r_alt != r1_c: r2_c = r_alt

        d2 = self.analisar_rota(r2_c, perfil)

        res = f"👤 UTILIZADOR: {self.usuario_atual.upper()} | 🏆 PONTOS: {self.model.utilizadores[self.usuario_atual]['pontos']}\n🩺 ESTADO FÍSICO: {perfil.upper()}\n" + "="*60 + "\n\n"
        
        if r1_c == r2_c: 
            d1["cor_hex"] = "#8e44ad"; d1["cor_nome"] = "ROXO"; self.rotas_temp = {"Caminho Único": d1}
            res += f"🌟 CAMINHO ÚNICO OTIMIZADO | 🗺️ COR NO MAPA: {d1['cor_nome']}\n" + self.formatar_relatorio(d1)
        else:
            d1["cor_hex"] = "#3498db"; d1["cor_nome"] = "AZUL"
            d2["cor_hex"] = "#e74c3c"; d2["cor_nome"] = "VERMELHO"
            ordem = [(d1, "Opção 1 (Preferencial)"), (d2, "Opção 2 (Alternativa)")]
            self.rotas_temp = {titulo: dados for dados, titulo in ordem}
            for dados, titulo in ordem:
                res += f"🌟 {titulo.upper()} | 🗺️ COR NO MAPA: {dados['cor_nome']}\n" + self.formatar_relatorio(dados) + "-"*55 + "\n\n"

        if "PERIGO" in d1["status"] and "PERIGO" in d2["status"]: res += "🚨 ALERTA: Rotas perigosas, decisão é sua."
        self.view.atualizar_opcoes_gamificacao(list(self.rotas_temp.keys()))
        self.view.atualizar_resultado(res)

    def concluir_rota(self):
        escolha = self.view.cb_escolha_rota.get()
        if not escolha or escolha not in self.rotas_temp:
            messagebox.showerror("Aviso", "Calcule e selecione uma rota primeiro.")
            return
            
        pts = self.rotas_temp[escolha]["pontos"]
        self.model.adicionar_pontos(self.usuario_atual, pts)
        
        if self.usuario_atual not in self.historico_sessao:
            self.historico_sessao[self.usuario_atual] = {"perfil": self.model.utilizadores[self.usuario_atual]["perfil"], "trajetos": [], "pontos_sessao": 0}
        self.historico_sessao[self.usuario_atual]["trajetos"].append(self.rotas_temp[escolha]["trajeto"])
        self.historico_sessao[self.usuario_atual]["pontos_sessao"] += pts
        
        messagebox.showinfo("Parabéns!", f"Caminho concluído! Ganhou {pts} pontos.\nTotal: {self.model.utilizadores[self.usuario_atual]['pontos']} pontos.")
        self.processar_rota()

    def mostrar_ranking(self):
        ranking = sorted(self.model.utilizadores.items(), key=lambda x: x[1]['pontos'], reverse=True)[:10]
        res = "🏆 TOP 10 - CLASSIFICAÇÃO GERAL 🏆\n" + "="*40 + "\n\n"
        for i, (nome, dados) in enumerate(ranking):
            medalha = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "👤"
            res += f"{medalha} {i+1}º Lugar: {nome} - {dados['pontos']} Pontos\n"
        self.view.atualizar_resultado(res)

    def formatar_relatorio(self, d):
        r = f"🛣️ Trajeto: {d['trajeto']}\n📏 1. Distância: {d['dist']:.2f} km\n⏱️ 2. Tempo: {d['tempo']:.1f} min\n"
        r += f"📐 3. Inclinação (Média: {d['inc']:.1f}% | Máx: {d['inc_max']:.1f}%)\n📈 4. Esforço: {d['esforco']}\n"
        r += f"🌳 5. Verde: {'★'*int(d['verde'])}{'☆'*(5-int(d['verde']))}\n🎯 6. PONTOS A GANHAR: {d['pontos']} pts\n"
        r += f"🦺 7. RECOMENDAÇÃO: {d['status']}\n📍 8. Detalhes:\n{d['detalhe']}\n\n"
        return r

    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EcoPathController()
    app.executar()