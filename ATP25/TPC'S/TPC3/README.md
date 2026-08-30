TPC2 Duarte Matos; A110102;
<img width="2316" height="3088" alt="image" src="https://github.com/user-attachments/assets/516625dd-18e1-475b-83b2-30cb285bbb34" />
Instruções: "- Crie uma aplicação em Python que coloca no monitor o seguinte menu:
    * (1) Criar Lista 
    * (2) Ler Lista
    * (3) Soma
    * (4) Média
    * (5) Maior
    * (6) Menor
    * (7) estaOrdenada por ordem crescente
    * (8) estaOrdenada por ordem decrescente
    * (9) Procura um elemento
    * (0) Sair
- O utilizador irá escolher uma das opções introduzindo o número correspondente;
- Se a opção não for sair, a aplicação executa a operação pretendida, apresenta o resultado e a seguir apresenta de novo o menu;
- Se a opção for sair, a aplicação termina colocando uma mensagem no monitor.

* No desenvolvimento da aplicação deverá ter em atenção o seguinte:
    - A aplicação terá uma variável interna para guardar uma lista de números;
    - Na opção 1, deverá ser criada uma lista de números aleatórios entre 1 e 100 que será guardada na variável interna;
    - Na opção 2, deverá ser criada uma lista com números introduzidos pelo utilizador, que será guardada na variável interna;
    - Nestas primeiras opções, se a variável interna já tiver uma lista, esta será sobreposta/apagada pela nova lista;
    - Na opção 3, será calculada a soma dos elementos na lista no momento;
    - Na opção 4, será calculada a média dos elementos na lista no momento;
    - Na opção 5, será calculado o maior elemento da lista no momento;
    - Na opção 6, será calculado o menor elemento da lista no momento;
    - Na opção 7, a aplicação deverá indicar (Sim/Não) se a lista está ordenada por ordem crescente;
    - Na opção 8, a aplicação deverá indicar (Sim/Não) se a lista está ordenada por ordem decrescente;
    - Na opção 9, a aplicação irá procurar um elemento na lista, se o encontrar deverá devolver a sua posição, devolverá -1 se o elemento não estiver na lista;
    - Se o utilizador selecionar a opção 0, a aplicação deverá terminar mostrando a lista que está nesse momento guardada."

Prints:
<img width="1602" height="1027" alt="comando1" src="https://github.com/user-attachments/assets/ec2b9235-362e-4ec8-b86b-72b84163ce28" />
<img width="1610" height="1050" alt="comando2" src="https://github.com/user-attachments/assets/5522162b-6c0a-40dd-acc2-8759f2e388d5" />
<img width="1608" height="1047" alt="comando3" src="https://github.com/user-attachments/assets/c504c6c2-a7d6-40d9-8941-95d080373de5" />
<img width="1608" height="1042" alt="comando4" src="https://github.com/user-attachments/assets/39da8bf5-50c3-420d-a1f1-d5bb64c2d2ea" />

Código:
"import random

def criaLista():
    N = int(input("Quantos números quer gerar?"))
    lista = []

    while len(lista) < N:
        lista.append(random.randint(1,100))
    return lista

def lelista():
    N = int(input("Quantos números queres adicionar à lista"))
    lista = []

    while len(lista) < N:
        lista.append(int(input(f"Adicione o {len(lista) + 1}º número! ")))
    return lista

def somaLista(lista):
    res = []
    i = 0
    for elem in lista:
        i=i+elem
        res.append(i)
    return i

def mediaLista(lista):
    res = 0
    for elem in lista:
        res = elem + res
    return res / len(lista)

def maiorelem(lista):
    res = lista[0] 
    for elem in lista[1:]:
        if elem > res:
            res = elem
        elif elem <= res:
            res = res
    return res

def menorLista(lista):
    res = lista[0]
    for elem in lista[1:]:
        if elem < res:
            res = elem
        elif elem >= res:
            res = res
    return res

def estaOrdenadaCrescente(lista):
    for i in range(len(lista) - 1):
        if lista[i] > lista[i + 1]:
            return "Não"
    return "Sim"

def estaOrdenadaDecrescente(lista):
    for i in range(len(lista) - 1):
        if lista[i] < lista[i + 1]:
            return "Não"
    return "Sim"


def procuraElemento(lista, elem):
    for i in range(len(lista)):
        if lista[i] == elem:
            return i  # devolve a posição onde encontrou
    return -1  # se não encontrar

while True:
    print("\n--- MENU ---")
    print("(1) Criar Lista (aleatória)")
    print("(2) Ler Lista (manual)")
    print("(3) Soma")
    print("(4) Média")
    print("(5) Maior")
    print("(6) Menor")
    print("(7) Está ordenada (crescente)?")
    print("(8) Está ordenada (decrescente)?")
    print("(9) Procurar elemento")
    print("(0) Sair")

    opcao = input("Escolha uma opção: ")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        lista_interna = criaLista()
        print("Lista criada:", lista_interna)

    elif opcao == "2":
        lista_interna = lelista()
        print("Lista criada:", lista_interna)

    elif opcao == "3":
        if lista_interna:
            print("Soma =", somaLista(lista_interna))
        else:
            print("Lista vazia!")

    elif opcao == "4":
        if lista_interna:
            print("Média =", mediaLista(lista_interna))
        else:
            print("Lista vazia!")

    elif opcao == "5":
        if lista_interna:
            print("Maior =", maiorelem(lista_interna))
        else:
            print("Lista vazia!")

    elif opcao == "6":
        if lista_interna:
            print("Menor =", menorLista(lista_interna))
        else:
            print("Lista vazia!")

    elif opcao == "7":
        if lista_interna:
            print(estaOrdenadaCrescente(lista_interna))
        else:
            print("Lista vazia!")

    elif opcao == "8":
        if lista_interna:
            print(estaOrdenadaDecrescente(lista_interna))
        else:
            print("Lista vazia!")

    elif opcao == "9":
        if lista_interna:
            elem = int(input("Elemento a procurar: "))
            pos = procuraElemento(lista_interna, elem)
            print(f"Posição: {pos}")
        else:
            print("Lista vazia!")

    elif opcao == "0":
        print("A sair... Lista final:", lista_interna)
        break

    else:
        print("Opção inválida! Tente de novo.")"





    



    



