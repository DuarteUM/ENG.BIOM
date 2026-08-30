[TurmaApp.py](https://github.com/user-attachments/files/23061663/TurmaApp.py)[Turma.py](https://github.com/user-attachments/files/23061658/Turma.py)TPC1 Duarte Matos; A110102;
<img width="2316" height="3088" alt="image" src="https://github.com/user-attachments/assets/600985d6-6f81-409e-82ef-2440f1f95aed" />
### TPC5: Aplicação para gestão de alunos

Considere que o modelo do aluno e da turma têm a seguinte estrutura:

`aluno = (nome, id, [notaTPC, notaProj, notaTeste])`

`turma = [aluno]`

* Cria uma aplicação que coloca no monitor o seguinte menu de operações:
    - 1: Criar uma turma;
    - 2: Inserir um aluno na turma;
    - 3: Listar a turma;
    - 4: Consultar um aluno por id;
    - 8: Guardar a turma em ficheiro;
    - 9: Carregar uma turma dum ficheiro;
    - 0: Sair da aplicação
* No fim de executar a operação selecionada, a aplicação deverá colocar novamente o menu e pedir ao utilizador a opção para continuar;
* Utiliza a tua aplicação para criar uma turma com 5 alunos.
  
_______________código:


  [Uploadin
def criarAluno(nome, id, notaTPC, notaProj, notaTeste):
    return (nome, id, [notaTPC, notaProj, notaTeste])
def criarTurma(turma):
    turma.clear()
    return turma
def menu():
    c=int(input("\n (1) Criar turma  \n (2) Inserir aluno \n (3) Listar a turma \n (4) Consultar aluno por id \n (8) Guardar turma em ficheiro \n (9) Carregar turma de ficheiro \n (0) Sair \n"))
    return c
def inserirAluno(turma):
    turma.append(criarAluno(input("Qual o nome do Aluno?"), input("Qual o id do aluno?"), float(input("Qual a nota do tpc?")),  float(input("Qual a nota do projeto?")),  float(input("Qual a nota do Teste?"))))
def listarTurma(turma):
    for e in turma:
        print(e)
    return
def consultarAluno(turma, id):
    i=0
    while i<len(turma):
        if id==turma[i][1]:
            return print(f"O Aluno com o id {id} é: {turma[i]}")   
        i+=1
    return print("Aluno nao encontrado")
        
def guardarTurma(turma,ficheiro):
    with open(ficheiro, "w") as f:
        for aluno in turma:
            nome, id, notas = aluno
            linha = f"{nome},{id},{notas[0]},{notas[1]},{notas[2]}\n"
            f.write(linha)

def carregarTurma(turma, ficheiro):
    turma.clear()
    with open(ficheiro, "r") as f:
        for linha in f:
            partes = linha.strip().split(",")
            nome = partes[0]
            id = partes[1]
            notas = [float(partes[2]), float(partes[3]), float(partes[4])]
            turma.append((nome, id, notas))
    return turma
g Turma.py…]()

_________código:

[Uploading Timport Turma as t
turma=[]
res=1
while res!= 0:
    res=t.menu()
    if res == 1:
        t.criarTurma(turma)
        print ("A turma foi criada vazia")
    if res == 2:
        t.inserirAluno(turma)
    if res == 3:
        t.listarTurma(turma)
    if res == 4:
        t.consultarAluno(turma, input("Introduza o id do aluno"))
    if res == 8:
        t.guardarTurma(turma, input("Introduz o Nome do ficheiro (.txt)"))  
    if res == 9:
        t.carregarTurma(turma, input("Introduz o Nome do ficheiro (.txt)") )
    if res == 0:
        break
    urmaApp.py…]()

___________ prints:

<img width="1316" height="591" alt="Tpc1" src="https://github.com/user-attachments/assets/482daa17-b906-4910-9fd4-aa87ed67eeb5" />

<img width="1307" height="1072" alt="Tpc2" src="https://github.com/user-attachments/assets/166326ee-44da-45f0-badc-2baeb8e77b10" />
[Turma.py](https://github.com/user-attachments/files/23061685/Turma.py)

