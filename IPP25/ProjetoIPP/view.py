import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class EcoPathView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("EcoPath")
        self.root.geometry("850x950")
        self.root.config(bg="white")
        
        self.container_principal = tk.Frame(self.root, bg="white")
        self.container_principal.pack(fill="both", expand=True)
        self.construir_login_interface()

    def construir_login_interface(self):
        for widget in self.container_principal.winfo_children(): widget.destroy()
            
        tk.Label(self.container_principal, text="EcoPath: Autenticação", font=("Arial", 22, "bold"), bg="white").pack(pady=20)
        self.abas = ttk.Notebook(self.container_principal)
        self.abas.pack(fill="both", expand=True, padx=40, pady=10)
        
        self.tab_entrar = tk.Frame(self.abas, bg="#f0f0f0", padx=20, pady=20)
        self.abas.add(self.tab_entrar, text="Entrar")
        tk.Label(self.tab_entrar, text="Selecione o seu Nome:", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 5))
        self.cb_login_user = ttk.Combobox(self.tab_entrar, state="readonly", font=("Arial", 11))
        self.cb_login_user.pack(fill="x", pady=(0, 15))
        tk.Label(self.tab_entrar, text="Palavra-passe (Password):", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(anchor="w", pady=(5, 5))
        self.ent_login_pass = tk.Entry(self.tab_entrar, show="*", font=("Arial", 11))
        self.ent_login_pass.pack(fill="x", pady=(0, 20))
        tk.Button(self.tab_entrar, text="Autenticar", font=("Arial", 12, "bold"), bg="#27ae60", fg="white", relief="flat", command=lambda: self.controller.processar_login(self.cb_login_user.get(), self.ent_login_pass.get())).pack(fill="x", pady=10)
        
        self.tab_registar = tk.Frame(self.abas, bg="#f0f0f0", padx=20, pady=20)
        self.abas.add(self.tab_registar, text="Registar")
        tk.Label(self.tab_registar, text="Nome e Apelido:", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 5))
        self.ent_reg_nome = tk.Entry(self.tab_registar, font=("Arial", 11))
        self.ent_reg_nome.pack(fill="x", pady=(0, 15))
        tk.Label(self.tab_registar, text="Indique a sua condição:", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(anchor="w", pady=(5, 5))
        
        condicoes = ["Asma", "Autismo", "Baixa Visão", "Cadeira de Rodas", "Cardiopata", "Criança", "Défice Cognitivo", "Diabetes", "Doença Articular", "Fibromialgia", "Grávida", "Idoso", "Invisual", "Jovem Saudável", "Lesão Temporária", "Muletas", "Obesidade", "Sedentário", "Surdez", "Vertigens"]
        self.cb_reg_handicap = ttk.Combobox(self.tab_registar, state="readonly", font=("Arial", 11), values=condicoes)
        self.cb_reg_handicap.pack(fill="x", pady=(0, 20))
        tk.Button(self.tab_registar, text="Gravar Registo", font=("Arial", 12, "bold"), bg="#2c3e50", fg="white", relief="flat", command=lambda: self.controller.processar_registo(self.ent_reg_nome.get(), self.cb_reg_handicap.get())).pack(fill="x", pady=10)

    def preencher_login_dropdown(self, utilizadores):
        nomes = sorted(list(utilizadores.keys()))
        self.cb_login_user['values'] = nomes
        if nomes: self.cb_login_user.current(0)

    def mostrar_ecran_principal(self, locais):
        for widget in self.container_principal.winfo_children(): widget.destroy()
            
        tk.Label(self.container_principal, text="EcoPath: Mobilidade e Recompensas", font=("Arial", 22, "bold"), bg="white").pack(pady=10)
        
        f = tk.Frame(self.container_principal, bg="#f0f0f0", padx=20, pady=10, relief="solid", bd=1)
        f.pack(fill="x", padx=40)
        
        tk.Label(f, text="Ponto de Partida Inicial:", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(anchor="w")
        self.cb_origem = ttk.Combobox(f, state="readonly", font=("Arial", 11), values=locais)
        self.cb_origem.pack(fill="x", pady=(0, 5))
        self.cb_origem.current(0)
        
        tk.Label(f, text="Destino Final:", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(anchor="w")
        self.cb_destino = ttk.Combobox(f, state="readonly", font=("Arial", 11), values=locais)
        self.cb_destino.pack(fill="x", pady=(0, 5))
        self.cb_destino.current(1)
        
        f_botoes = tk.Frame(self.container_principal, bg="white")
        f_botoes.pack(fill="x", padx=40, pady=5)
        tk.Button(f_botoes, text="🗺️ Abrir Mapa", font=("Arial", 11), bg="#2c3e50", fg="white", command=self.controller.abrir_mapa).pack(side="left", expand=True, fill="x", padx=(0,5))
        tk.Button(f_botoes, text="🏆 Ver Ranking (Top 10)", font=("Arial", 11, "bold"), bg="#8e44ad", fg="white", command=self.controller.mostrar_ranking).pack(side="right", expand=True, fill="x", padx=(5,0))
        
        tk.Button(self.container_principal, text="CALCULAR E COMPARAR ROTAS ➔", font=("Arial", 13, "bold"), bg="#27ae60", fg="white", command=self.controller.processar_rota).pack(pady=10, fill="x", padx=40)
        
        f_gamificacao = tk.Frame(self.container_principal, bg="white")
        f_gamificacao.pack(fill="x", padx=40, pady=5)
        tk.Label(f_gamificacao, text="Escolher Percurso:", bg="white", font=("Arial", 10, "bold")).pack(side="left")
        self.cb_escolha_rota = ttk.Combobox(f_gamificacao, state="readonly", font=("Arial", 10))
        self.cb_escolha_rota.pack(side="left", fill="x", expand=True, padx=10)
        tk.Button(f_gamificacao, text="✓ Concluir e Ganhar Pontos", font=("Arial", 10, "bold"), bg="#f39c12", fg="white", command=self.controller.concluir_rota).pack(side="right")
        
        scroll_frame = tk.Frame(self.container_principal)
        scroll_frame.pack(padx=40, pady=10, fill="both", expand=True)
        self.txt_resultado = tk.Text(scroll_frame, font=("Consolas", 10), wrap="word", relief="solid", bd=1)
        self.txt_resultado.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(scroll_frame, command=self.txt_resultado.yview)
        scrollbar.pack(side="right", fill="y")
        self.txt_resultado.config(yscrollcommand=scrollbar.set)

    def atualizar_opcoes_gamificacao(self, opcoes):
        self.cb_escolha_rota['values'] = opcoes
        if opcoes: self.cb_escolha_rota.current(0)

    def atualizar_resultado(self, texto):
        self.txt_resultado.delete(1.0, tk.END)
        self.txt_resultado.insert(tk.END, texto)

    def desenhar_mapa(self, segmentos, rotas_calculadas=None):
        coords = {
            "Estádio": (10, 90), "Hospital": (85, 90), "Bom Jesus": (100, 100),
            "UMinho": (80, 70), "Praça Central": (50, 50), "Sameiro": (100, 15),
            "Sé": (38, 42), "Estação": (8, 50), "Arco da Porta Nova": (28, 52),
            "Centro Comercial": (75, 58), "Jardim Municipal": (55, 68), "Rio Este": (50, 5),
            "Teatro Principal": (65, 48), "Biblioteca": (45, 28), "Parque Norte": (12, 78),
            "Mercado Central": (12, 18), "Museu de Arte": (32, 62)
        }
        fig, ax = plt.subplots(figsize=(12, 10))
        fig.patch.set_facecolor('#dcdde1')
        ax.set_facecolor('#dcdde1')
        ax.add_patch(patches.Circle((100, 100), 16, color='#27ae60', alpha=0.5)) 
        ax.add_patch(patches.Circle((100, 15), 14, color='#27ae60', alpha=0.5)) 
        ax.add_patch(patches.Rectangle((50, 62), 12, 12, color='#2ecc71', alpha=0.4)) 
        ax.add_patch(patches.Rectangle((5, 75), 18, 12, color='#2ecc71', alpha=0.4)) 
        ax.plot([0, 100], [5, 12], color='#3498db', lw=10, alpha=0.7)
        
        for s in segmentos:
            if s["origem"] in coords and s["destino"] in coords:
                o, d = coords[s["origem"]], coords[s["destino"]]
                ax.plot([o[0], d[0]], [o[1], d[1]], color='black', lw=1.5, zorder=3, alpha=0.3)
                
        if rotas_calculadas:
            for titulo, dados in rotas_calculadas.items():
                nodos = dados["nodos"]
                cor = dados.get("cor_hex", "blue")
                for i in range(len(nodos)-1):
                    o = coords[nodos[i]]
                    d = coords[nodos[i+1]]
                    ax.plot([o[0], d[0]], [o[1], d[1]], color=cor, lw=5, zorder=4, alpha=0.8)

        for loc, (x, y) in coords.items():
            ax.scatter(x, y, s=350, c="black", edgecolors="white", zorder=5)
            ax.text(x, y+3.5, loc, ha="center", color="black", fontweight="bold", fontsize=11, zorder=6)
            
        plt.title("MAPA CARTOGRÁFICO DE BRAGA", fontsize=18, fontweight='bold')
        plt.axis("off")
        plt.tight_layout()
        plt.show()