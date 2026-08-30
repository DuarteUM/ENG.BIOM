import FreeSimpleGUI as sg
import clinic
import plots
import numpy as np
import random

DADOS_PESSOAS = clinic.carregar_base_dados_pessoas("pessoas (1).json")

def formatar_tempo(minutos_decimais):
    horas = int(minutos_decimais // 60)
    minutos = int(minutos_decimais % 60)
    segundos = int((minutos_decimais * 60) % 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def criar_layout(tema="Claro"):
    cor_titulo = "#000080" if tema == "Claro" else "#FFD700" 
    cor_fundo_multiline = "#F0F0F0" if tema == "Claro" else "#2D2D2D"
    cor_texto_multiline = "black" if tema == "Claro" else "white"
    
    layout = [
        [sg.Text("SIMULAÇÃO DE CLÍNICA MÉDICA", font=("Helvetica", 16, "bold"), text_color=cor_titulo), 
         sg.Push(), 
         sg.Text("Modo:"), sg.Combo(["Claro", "Escuro"], default_value=tema, key="-MODO-", enable_events=True, readonly=True)],
        [sg.HorizontalSeparator()],
        [sg.Frame("Configuração de Parâmetros", [
            [sg.Text("Médicos:"), sg.Input("3", key="-MEDICOS-", size=(6,1)), 
             sg.Text("Taxa (doentes/h):"), sg.Input("10", key="-TAXA-", size=(6,1))],
            [sg.Text("Consulta (min):"), sg.Input("15", key="-CONSULTA-", size=(6,1)),
             sg.Text("Duração (min):"), sg.Input("480", key="-DURACAO-", size=(6,1))],
            [sg.Text("Distribuição:"), sg.Combo(["exponential", "normal", "uniform"], default_value="exponential", key="-DIST-", readonly=True)]
        ])],
        [sg.Button("EXECUTAR SIMULAÇÃO", button_color=("white", "#2c3e50"), size=(30, 2), pad=(0,10))],
        [sg.Frame("Análise Gráfica Principal", [
            [sg.Button("Gráfico: Evolução da Fila"), sg.Button("Gráfico: Ocupação"), sg.Button("Gráfico: Correlação (10-30)")]
        ], pad=(0,10))],
        [sg.Frame("Análise de Perfil", [
            [sg.Button("Faixas Etárias"), sg.Button("Triagem de Manchester")]
        ], pad=(0,10))],
        [sg.Text("Relatório de Atendimento:", font=("Helvetica", 10, "bold"))],
        [sg.Multiline(size=(75, 12), key="-OUT-", font=("Courier New", 10), 
                     background_color=cor_fundo_multiline, text_color=cor_texto_multiline, disabled=True)]
    ]
    return layout

sg.theme("SystemDefault")
window = sg.Window("Clínica Médica - Engenharia Biomédica", criar_layout("Claro"), finalize=True)

stats_fixos = None 
correlacao_x, correlacao_y = [], []

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: break

    if event == "-MODO-":
        tema_escolhido = values["-MODO-"]
        if tema_escolhido == "Escuro":
            sg.theme("DarkGrey11")
        else:
            sg.theme("SystemDefault")
        
        loc = window.current_location()
        window.close()
        window = sg.Window("Clínica Médica - Engenharia Biomédica", criar_layout(tema_escolhido), location=loc, finalize=True)
        continue

    if event == "EXECUTAR SIMULAÇÃO":
        try:
            n_med, taxa, t_cons, dur, dist = int(values["-MEDICOS-"]), float(values["-TAXA-"]), float(values["-CONSULTA-"]), float(values["-DURACAO-"]), values["-DIST-"]
            
            if n_med <= 0 or taxa <= 0 or t_cons <= 0 or dur <= 0:
                sg.popup_error("Erro: Os valores devem ser superiores a zero.")
                continue

            stats_fixos, _ = clinic.simula(n_med, taxa, t_cons, dur, dist, DADOS_PESSOAS)
            
            correlacao_x = list(range(10, 31, 2))
            correlacao_y = [np.mean(clinic.simula(n_med, t, t_cons, dur, dist, DADOS_PESSOAS)[0]["timeline_fila"]) for t in correlacao_x]
            
            total = stats_fixos["atendidos"]
            esp_med_formatado = formatar_tempo(np.mean(stats_fixos["espera"])) if total > 0 else "00:00:00"
            sat_media = np.mean(stats_fixos["satisfacao_individual"]) if total > 0 else 0
            
            output = f"{'='*40}\n ESTATÍSTICAS GERAIS\n{'='*40}\n"
            output += f" Doentes Atendidos: {total}\n"
            output += f" Tempo Médio de Espera: {esp_med_formatado} (HH:MM:SS)\n"
            output += f" Taxa de Ocupação Médica: {stats_fixos['ocupacao_media']:.2f}%\n\n"
            
            output += f"{'='*40}\n TRIAGEM DE MANCHESTER\n{'='*40}\n"
            output += f" Vermelhos: {stats_fixos['cores_atendidas'].count('vermelha')} | Laranjas: {stats_fixos['cores_atendidas'].count('laranja')}\n"
            output += f" Amarelos:  {stats_fixos['cores_atendidas'].count('amarela')} | Verdes:   {stats_fixos['cores_atendidas'].count('verde')}\n\n"
            
            output += f"{'='*40}\n PERFIL DE SAÚDE\n{'='*40}\n"
            output += f" Média de Idades: {np.mean(stats_fixos['idades']):.1f} anos\n"
            output += f" Sexo: M:{stats_fixos['sexos'].count('masculino')/total*100:.1f}% | F:{stats_fixos['sexos'].count('feminino')/total*100:.1f}% | Outros:{stats_fixos['sexos'].count('outro')/total*100:.1f}%\n"
            output += f" Nível de Satisfação: {sat_media:.1f}%\n"
            output += f"{'='*40}\n"
            window["-OUT-"].update(output)
            
        except ValueError:
            sg.popup_error("Por favor, insira valores válidos.")

    if event == "Gráfico: Evolução da Fila" and stats_fixos:
        plots.mostrar_grafico_fila(stats_fixos)
    
    if event == "Gráfico: Ocupação" and stats_fixos:
        plots.mostrar_grafico_ocupacao(stats_fixos)
    
    if event == "Gráfico: Correlação (10-30)" and correlacao_y:
        plots.mostrar_grafico_correlacao(correlacao_x, correlacao_y)
    
    if event == "Faixas Etárias" and stats_fixos:
        plots.mostrar_grafico_faixas_etarias(stats_fixos["idades"])
    
    if event == "Triagem de Manchester" and stats_fixos:
        plots.mostrar_grafico_manchester(stats_fixos["cores_atendidas"])

window.close()