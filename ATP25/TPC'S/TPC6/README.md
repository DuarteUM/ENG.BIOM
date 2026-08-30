TPC1 Duarte Matos; A110102;
<img width="2316" height="3088" alt="image" src="https://github.com/user-attachments/assets/2f9ddd5a-8e9b-4b34-8b91-5d1ce1dd67fd" />
Cria uma aplicação Python que permita ao utilizador usar todas as funcionalidades como: 
 1- Temperatura media 
 2- Guardar Tabela 
 3- Carregar tabela 
 4- Temperatura minima 
 5- Amplitude termica 
 6- Precipitaçao Maxima 
 7- Dias com precipitaçao acima de x 
 8- Numero consecutivo de dias com precipitaçao abaixo de X 
 9- Grafico da tabela 
 0- Sair

 
 <img width="1530" height="581" alt="image" src="https://github.com/user-attachments/assets/cd225e54-1d1a-4787-a222-146a3c0423a7" />


______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
 
[MetereologiaApp.py](https://github.com/user-attachments/files/23219153/MetereologiaApp.py)
import Metereologia as met
tabMeteo = [((2022,1,20), 2, 16, 0),((2022,1,21), 1, 13, 0.2), ((2022,1,22), 7, 17, 0.01)]

i=met.menu()

while i != 0:
    if i==1:
        print(met.medias(tabMeteo))
    elif i==2:
        met.guardaTabMeteo(tabMeteo, "metereologia.txt")
        print("A tabela foi guardada no ficheiro metereologia.txt")
    elif i==3:
        tabMeteo=met.carregaTabMeteo("metereologia.txt")
        print(tabMeteo)
    elif i==4:
        print(met.minMin(tabMeteo))
    elif i==5:
        print(met.amplTerm(tabMeteo))
    elif i==6:
        print(met.maxChuva(tabMeteo))
    elif i==7:
        print(met.diasChuvosos(tabMeteo, float(input("Escolhe o valor limite"))))
    elif i==8:
        print(met.maxPeriodoCalor(tabMeteo, float(input("Escreva o limite desejado"))))
    elif i==9:
        met.grafTabMeteo(tabMeteo)
    i=met.menu()


______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

  [Metereologia.py](https://github.com/user-attachments/files/23219214/Metereologia.py)
import matplotlib.pyplot as plt

def medias(tabMeteo):
    res = []
    x=0
    while x< len(tabMeteo):
        med= (tabMeteo[x][1]+ tabMeteo[x][2])/2
        res.append((tabMeteo[x][0], med))
        x+=1
    return res

def guardaTabMeteo(t, fnome):
    f = open(fnome, "w", encoding='utf-8')
    for dia in t:
        data, tempMin, tempMax, prec = dia
        linha = f"{data[0]},{data[1]},{data[2]},{tempMin},{tempMax},{prec}\n"
        f.write(linha)
    f.close()
    return

def carregaTabMeteo(fnome):
    res = []
    f= open(fnome, encoding='utf-8')
    for linha in f:
        campos=linha.split(",")
        res.append(((int(campos[0]),int(campos[1]),int(campos[2])), float(campos[3]), float(campos[4]), float(campos[5])))
    f.close()
    return res

def minMin(tabMeteo):
    minima=tabMeteo[0][1]
    i=0
    while i<len(tabMeteo):
        if minima>tabMeteo[i][1]:
            minima=tabMeteo[i][1]
        i+=1
    return minima

def amplTerm(tabMeteo):
    res=[]
    for e in tabMeteo:
        res.append((e[0],e[2]-e[1]))
    return res 

def maxChuva(tabMeteo):
    max_prec=tabMeteo[0][3]
    i=0
    while i<len(tabMeteo):
        if max_prec<tabMeteo[i][3]:
            max_prec=tabMeteo[i][3]
            max_data=tabMeteo[i][0]
        i+=1
    return (max_data, max_prec)

def diasChuvosos(tabMeteo, p):
    res=[]
    print(p)
    for e in tabMeteo:
        if e[3]>=p:
            res.append((e[0],e[3]))
    return res

def maxPeriodoCalor(tabMeteo, p):
    res=0
    max=0
    for e in tabMeteo:
        if e[3]<p:
            res+=1
        else:
            if max <=res:
                max=res
    if max ==0:
        return res
    else:
        return max

def extraiTMin(t):
    res=[]
    for _,tmin,_,_ in t:
        res.append(tmin)
    return res

def extraiTMax(t):
    res=[]
    for _,_,tmax,_ in t:
        res.append(tmax)
    return res

def extraiPrecip(t):
    res=[]
    for _,_,_,precip in t:
        res.append(precip)
    return res

def grafTabMeteo(t):
    #Tmin
    x1 = list(range(1,len(t)+1))
    y1= extraiTMin(t)
    plt.plot(x1,y1, label="Tempreatura Minima")

    #Tmax
    x2 = list(range(1,len(t)+1))
    y2= extraiTMax(t)
    plt.plot(x2,y2, label="Tempreatura Maxima")
    
    #Precip
    x3=  list(range(1,len(t)+1))
    y3= extraiPrecip(t)
    plt.plot(x3,y3, label="Tempreatura Maxima")

    plt.title("Metrologia")
    plt.legend()
    plt.show()
    return

def menu():
    return int(input(f" 1- Temperatura media \n 2- Guardar Tabela \n 3- Carregar tabela \n 4- Temperatura minima \n 5- Amplitude termica \n 6- Precipitaçao Maxima \n 7- Dias com precipitaçao acima de x \n 8- Numero consecutivo de dias com precipitaçao abaixo de X \n 9- Grafico da tabela \n 0- Sair \n"))
