# Relatório Técnico Final: Simulação de Clínica Médica
**Projeto Laboratorial - Engenharia Biomédica (2º Ano)** **Unidade Curricular:** Algoritmos e Técnicas de Programação  
**Instituição:** Universidade do Minho / Escola de Engenharia  
**Coordenação:** José Carlos Ramalho e Luís Filipe Cunha  
**Data de Execução:** Novembro de 2025 - Janeiro de 2026

---

## 1. Introdução
Este projeto visa a modelação computacional e simulação de um ambiente clínico real, utilizando a metodologia de Simulação de Eventos Discretos (DES). O sistema desenvolvido permite estudar o comportamento de filas de espera, a ocupação de recursos médicos e a satisfação dos utentes sob diferentes condições de pressão (taxas de chegada). A solução integra um motor de simulação estocástico, uma interface gráfica interativa e um módulo de análise de dados.

---

## 2. Objetivos do Projeto
O principal objetivo foi a construção de uma ferramenta capaz de simular o fluxo de atendimento de doentes, cumprindo os seguintes requisitos pedagógicos e técnicos:
* **Modelação Estocástica:** Implementação de chegadas segundo uma distribuição de Poisson e tempos de serviço variáveis (Exponencial, Normal, Uniforme).
* **Gestão de Recursos:** Monitorização de filas de espera e ocupação de médicos.
* **Análise de Sensibilidade:** Capacidade de testar "cenários 10-30" (variação da taxa de chegada) para observar o comportamento exponencial da fila.
* **Visualização de Dados:** Geração de gráficos evolutivos e estatísticos para suporte à decisão.

---

## 3. Arquitetura do Sistema
A aplicação foi estruturada de forma modular para garantir a separação entre a lógica de negócio, a interface e a visualização.

### 3.1. Módulo de Simulação (clinic.py)
Este é o "motor" do sistema. A função simula gere o relógio da simulação e a lista de eventos (Queue de Eventos).
* **Lógica de Prioridade (Protocolo de Manchester Adaptado):**
Ao contrário de uma fila FIFO (First-In, First-Out) simples, o sistema implementa uma fila prioritária baseada na gravidade clínica. A gravidade é atribuída probabilisticamente:
    * **Vermelha (Emergência):** Prioridade 0. Atribuída se a frequência cardíaca (simulada) for <50 ou >100, ou através de uma combinação de testes booleanos aleatórios.
    * **Laranja (Muito Urgente):** Prioridade 1.
    * **Amarela (Urgente):** Prioridade 2.
    * **Verde (Pouco Urgente):** Prioridade 3.  
    *Implementação:* A fila é reordenada dinamicamente `fila.sort(key=lambda x: (x['prioridade'], x['tempo']))` sempre que um novo doente entra, garantindo que casos graves passem à frente.

* **Fatores de Envelhecimento:**
Foi introduzida uma regra de negócio específica onde doentes idosos (> 65 anos) requerem, em média, 20% mais tempo de consulta. Isto adiciona realismo ao modelo, impactando a ocupação dos médicos quando a demografia dos doentes é mais envelhecida.

* **Estrutura de Dados dos Doentes:**
Os doentes não são apenas números. O sistema carrega um dataset real (`pessoas (1).json`), permitindo associar nomes, idades e géneros aos eventos, o que enriquece a análise demográfica posterior.

### 3.2. Interface Gráfica (gui_app.py)
Desenvolvida com FreeSimpleGUI, a interface permite a configuração em tempo real sem necessidade de alterar o código fonte.
* **Funcionalidades de Controlo:**
    * Configuração de parâmetros: Nº de Médicos, Taxa de Chegada, Tempo Médio de Consulta e Duração da Simulação.
    * Seleção de Distribuição Estatística: Exponencial, Normal ou Uniforme.
    * Modo Escuro/Claro: O utilizador pode alternar o tema visual da aplicação dinamicamente.
* **Feedback Imediato:** Um painel de relatório apresenta, após a execução, os KPIs (Key Performance Indicators) principais: média de idades, distribuição de sexos e contagem por cor de triagem.

### 3.3. Módulo de Visualização (plots.py)
Utiliza a biblioteca matplotlib para gerar quatro tipos de visualizações essenciais:
* **Evolução da Fila:** Um gráfico de linha preenchido que mostra os picos de afluência ao longo do tempo.
* **Ocupação Médica:** Gráfico degrau (step plot) que visualiza a percentagem de médicos ocupados a cada minuto.
* **Correlação Taxa/Fila:** Executa múltiplas simulações em background variando a taxa de chegada de 10 a 30, demonstrando o ponto de rutura do sistema.
* **Distribuição Demográfica e Clínica:** Gráficos de barras para faixas etárias e gráficos circulares (pie charts) para as cores de Manchester.

---

## 4. Manual de Utilização e Parâmetros

### 4.1. Pré-requisitos
O sistema requer Python 3.8+ e as seguintes bibliotecas:
* Numpy 
* Matplotlib 
* FreeSimpleGUI

### 4.2. Configuração de Inputs
Na interface da aplicação, o utilizador deve definir:
* **Quantidade de medicos:** Numero de proficionais de saude disponiveis.
* **Taxa Chegada:** Parâmetro labda de Poisson. Define a "pressão" sobre a clínica.
* **Tempo Consulta:** Média da distribuição a selecionar. Base para o cálculo do tempo de serviço.
* **Distribuição:** Modelo matemático do tempo de serviço. Exponencial, Normal e Uniforme.

---

## 5. Análise de Resultados e Métricas
O sistema gera um relatório textual e gráfico que permite responder às questões levantadas no enunciado:

### 5.1. Impacto da Taxa de Chegada (Cenário de Stress)
Ao aumentar a taxa de chegada de 10 para 30 doentes/h, mantendo 3 médicos, observa-se que o tamanho da fila não cresce linearmente, mas sim exponencialmente. Isto valida a teoria de filas, onde a aproximação da taxa de utilização a 100% causa tempos de espera que tendem para infinito.

### 5.2. Eficiência da Triagem de Manchester
A introdução da prioridade por cores demonstrou que, em cenários de alta ocupação, os doentes "Verdes" e "Amarelos" são penalizados com tempos de espera significativamente superiores, enquanto os "Vermelhos" mantêm tempos de espera próximos de zero, validando a segurança clínica do modelo.

### 5.3. Indicadores Calculados
* **Satisfação Individual:** Calculada através da fórmula $100 - (EsperaReal - 10) * 1.5$, penalizando esperas superiores a 10 minutos.
* **Ocupação Média:** Somatorio do tempo trabalhado / (Numero de medicos * Tempo Simulação)

---

## 6. Análise de Resultados e Discussão
A análise dos dados gerados pela simulação permitiu identificar padrões comportamentais críticos no funcionamento da clínica. Abaixo, discutem-se os principais resultados obtidos, correlacionando as métricas de desempenho com os parâmetros configurados.

### 6.1. O Efeito do "Gargalo" (Análise de Sensibilidade)
Foi realizado um teste de stress variando a taxa de chegada de 10 para 30 doentes/hora, mantendo fixos 3 médicos e um tempo médio de consulta de 15 minutos.
* **Resultado Observado:** A relação entre a taxa de chegada e o tamanho da fila não é linear.
* **Discussão:** Observa-se que, enquanto se manter a capacidade nominal de atendimento, a fila mantém-se próxima de zero. Contudo, assim que a taxa de chegada se aproxima da capacidade máxima de atendimento dos médicos (Nº medicos * (60/15)), a fila cresce exponencialmente. Este comportamento valida a teoria de filas, demonstrando que pequenas variações na procura, quando o sistema está perto da saturação (ocupação > 85%), resultam em tempos de espera catastróficos.

### 6.2. Impacto da Triagem de Manchester na Equidade
A implementação do sistema de prioridades (Vermelho=0 a Verde=3) alterou drasticamente a distribuição do tempo de espera.
* **Resultado:** Doentes com pulseira Vermelha ou Laranja apresentaram tempos de espera consistentemente nulos ou residuais, mesmo em cenários de alta ocupação. Em contrapartida, doentes Verdes sofreram um aumento desproporcional na espera, sendo frequentemente ultrapassados na fila.
* **Implementação:** Isto deve-se à reordenação dinâmica da fila implementada no algoritmo, que garante que a gravidade clínica se sobrepõe à ordem de chegada.

### 6.3. Influência Demográfica na Eficiência (Fator Idade)
Uma descoberta interessante do modelo prende-se com o perfil etário dos doentes.
* **Resultado:** Simulações com uma média de idades superior resultaram numa menor quantidade de doentes atendidos por hora.
* **Causa:** O algoritmo implementa uma penalização de tempo para doentes idosos: `media_ajustada = mean_service_time * 1.2 if idade > 65`. Isto significa que um afluxo de doentes geriátricos reduz a capacidade efetiva da clínica em 20%, um dado crucial para o planeamento de recursos em zonas envelhecidas.

### 6.4. Análise da Satisfação do Utente
A métrica de satisfação revelou-se um indicador sensível à qualidade do serviço.
* **Métrica:** A satisfação foi modelada pela fórmula $S = 100 - (EsperaReal - 10) * 1.5$.
* **Interpretação:** O modelo assume uma tolerância de 10 minutos. A partir desse limiar, a satisfação decai linearmente a uma taxa de 1.5% por minuto.
* **Conclusão:** Para manter uma satisfação média positiva (>50%), o tempo de espera não pode exceder os 43 minutos. Este indicador ajuda a definir os níveis de serviço aceitáveis para a gestão da clínica.

---

## 7. Conclusões e Trabalho Futuro
A simulação cumpriu com sucesso os objetivos de modelar um sistema complexo com recursos limitados. A ferramenta permite aos gestores hospitalares prever quantos médicos são necessários para um determinado fluxo de doentes, garantindo níveis de serviço aceitáveis.

Anexamos agora uma seria de graficos que sao possiveis de obter na nosssa simulaçao. Numa fase inicial usamos como valores: 3 Medicos, 10 doentes por horas, 15 minutos de duração de consulta e 480 minutos de simulação 

![1](https://github.com/user-attachments/assets/ed7adc46-c8da-4a22-9e1c-45a74029c23b)
![2](https://github.com/user-attachments/assets/eb9bca49-b414-4131-a4ef-205c0a26a932)
![3](https://github.com/user-attachments/assets/a79398f7-313c-40d3-9804-2e2d3fd1d968)
![4](https://github.com/user-attachments/assets/d8e323a8-536b-4425-aff1-c1da177b66d3)
![5](https://github.com/user-attachments/assets/0ab129cc-8cc3-4221-b923-fe1de330c142)

Agora, numa segunda fase, aumentamos os medicos para 5 de modo a observar as alteraçoes nos graficos de maior relevancia.

![6](https://github.com/user-attachments/assets/9df87d6c-d5f3-4ca1-9056-5b5ac705f538)
![7](https://github.com/user-attachments/assets/154c8a0e-2df3-465a-9ff8-3793189ad13d)

**Projeto realizado por:** Afonso Faria (a111747), Duarte Matos (a110102), Simão Ribeiro (a111844).
