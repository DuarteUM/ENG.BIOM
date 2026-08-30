TPC1 Duarte Matos; A110102;
<img width="2316" height="3088" alt="image" src="https://github.com/user-attachments/assets/006e462c-13f1-4b44-92e8-b8980464979f" />
Realizar o teste de aferição da TP7
[TPC7.ipynb](https://github.com/user-attachments/files/23393111/TPC7.ipynb)
{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "a42c935e",
   "metadata": {},
   "source": [
    "#### a) Lista formada pelos elementos que não são comuns às duas listas:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "d35631a2",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[1, 2, 3, 6, 7, 8]\n"
     ]
    }
   ],
   "source": [
    "lista1 = [1, 2, 3, 4, 5]\n",
    "lista2 = [4, 5, 6, 7, 8]  \n",
    "ncomuns = []\n",
    "\n",
    "for e in lista1:\n",
    "    if e not in lista2:\n",
    "        ncomuns.append(e)\n",
    "for e in lista2:\n",
    "    if e not in lista1:\n",
    "        ncomuns.append(e)\n",
    "\n",
    "print(ncomuns)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "205d73f5",
   "metadata": {},
   "source": [
    "#### b) Lista formada pelas palavras do texto compostas por mais de 3 letras:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "e0247632",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['Vivia', 'poucos', 'anos', 'algures', 'concelho', 'Ribatejo', 'pequeno', 'lavrador', 'negociante', 'gado', 'chamado', 'Manuel', 'Peres', 'Vigário']\n"
     ]
    }
   ],
   "source": [
    "texto = \"\"\"Vivia há já não poucos anos algures num concelho do Ribatejo \n",
    "    um pequeno lavrador e negociante de gado chamado Manuel Peres Vigário\"\"\"\n",
    "lista = []\n",
    "\n",
    "for e in texto.split( ):\n",
    "    if len(e)>3:\n",
    "        lista.append(e)\n",
    "\n",
    "print(lista)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "878f36f6",
   "metadata": {},
   "source": [
    "#### c) Lista formada por pares do tipo (índice, valor) com os valores da lista dada:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "74a3858e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[(0, 'anaconda'), (1, 'burro'), (2, 'cavalo'), (3, 'macaco')]\n"
     ]
    }
   ],
   "source": [
    "lista = ['anaconda', 'burro', 'cavalo', 'macaco']\n",
    "listaRes = [(i, palavra) for i, palavra in enumerate(lista)]\n",
    "print(listaRes)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cafe3d75",
   "metadata": {},
   "source": [
    "### tpc-2"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "74c089e2",
   "metadata": {},
   "source": [
    "#### a) Especifique uma função que dada uma string e uma substring não vazia, calcula  o número de vezes em que a substring aparece na string, sem que haja sobreposição de substrings:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b796ba86",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2\n",
      "1\n",
      "0\n"
     ]
    }
   ],
   "source": [
    "def strCount(string, palavra):\n",
    "    res = 0\n",
    "    i = 0\n",
    "    while i <= len(string) - len(palavra):\n",
    "        if string[i:i+len(palavra)] == palavra:\n",
    "            res += 1\n",
    "            i += len(palavra)\n",
    "        else:\n",
    "            i += 1\n",
    "    print(res)\n",
    "\n",
    "strCount(\"catcowcat\", \"cat\") \n",
    "strCount(\"catcowcat\", \"cow\") \n",
    "strCount(\"catcowcat\", \"dog\") "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "05ad6016",
   "metadata": {},
   "source": [
    "#### b) Especifique uma função que recebe uma lista de números inteiros positivos e devolve o menor produto que for possível calcular multiplicando os 3 menores inteiros da lista:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4aed1579",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "168\n"
     ]
    }
   ],
   "source": [
    "def produtoM3(lista):\n",
    "    menores = sorted(lista)[:3]  \n",
    "    produto = menores[0] * menores[1] * menores[2]\n",
    "    return produto\n",
    "\n",
    "print(produtoM3([12,3,7,10,12,8,9]))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "604d6ec1",
   "metadata": {},
   "source": [
    "#### c) Especifique uma função que dado um número inteiro positivo, repetidamente adiciona os seus dígitos até obter apenas um dígito que é retornado como resultado:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8903d037",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "3\n"
     ]
    }
   ],
   "source": [
    "\n",
    "def reduxInt(n):\n",
    "    while n >= 10:\n",
    "        n = sum(int(d) for d in str(n))\n",
    "    return n\n",
    "\n",
    "print(reduxInt(777))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b490196e",
   "metadata": {},
   "source": [
    "#### d) Especifique uma função que recebe duas strings, `string1` e `string2`, e devolve o índice da primeira ocorrência de `string2` em `string1`, caso não ocorra nenhuma vez a função deverá retornar `-1`:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "33e25358",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "13\n",
      "-1\n"
     ]
    }
   ],
   "source": [
    "\n",
    "def myIndexOf(s1, s2):\n",
    "    for i in range(len(s1) - len(s2) + 1):\n",
    "        if s1[i:i+len(s2)] == s2:\n",
    "            return i\n",
    "    return -1\n",
    "print(myIndexOf(\"Hoje está um belo dia de sol!\", \"belo\"))  \n",
    "print(myIndexOf(\"Hoje está um belo dia de sol!\", \"chuva\")) "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "442e6e3c",
   "metadata": {},
   "source": [
    "#### Tpc 3\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "87b711b6",
   "metadata": {},
   "source": [
    "#### a) `quantosPost`, que indica quantos posts estão registados:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "b34d1098",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1\n"
     ]
    }
   ],
   "source": [
    "MyFaceBook = [{\n",
    "    'id': 'p1', \n",
    "    'conteudo': 'A tarefa de avaliação é talvez a mais ingrata das tarefas que um professortem de realizar...', \n",
    "    'autor': 'jcr', \n",
    "    'dataCriacao': '2023-07-20', \n",
    "    'comentarios': [\n",
    "        {\n",
    "            'comentario': 'Completamente de acordo...',\n",
    "            'autor': 'prh'\n",
    "        },\n",
    "        {\n",
    "            'comentario': 'Mas há quem goste...',\n",
    "            'autor': 'jj'\n",
    "        }]}]\n",
    "        \n",
    "def quantosPost(redeSocial):\n",
    "    return len(redeSocial)\n",
    "\n",
    "print(quantosPost(MyFaceBook))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ed4f212f",
   "metadata": {},
   "source": [
    "#### b)  `postsAutor`, que devolve a lista de posts de um determinado autor:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "bad1f462",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "A tarefa de avaliação é talvez a mais ingrata das tarefas que um professortem de realizar...\n",
      "\n"
     ]
    }
   ],
   "source": [
    "def postsAutor(redeSocial, autor):\n",
    "    for e in redeSocial:\n",
    "        if autor==e[\"autor\"]:\n",
    "            print(f\"{e[\"conteudo\"]}\\n\")\n",
    "    return \n",
    "\n",
    "postsAutor(MyFaceBook, input(\"Qual o nome do Autor:\"))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9594ae03",
   "metadata": {},
   "source": [
    "#### c) `autores`, que devolve a lista de autores de posts ordenada alfabeticamente:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "c072d8e1",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['jcr']\n"
     ]
    }
   ],
   "source": [
    "def autores(redeSocial):\n",
    "    res=[]\n",
    "    for e in redeSocial:\n",
    "        res.append(e[\"autor\"])\n",
    "    res.sort()\n",
    "    return res\n",
    "\n",
    "print(autores(MyFaceBook))\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cc99ffc0",
   "metadata": {},
   "source": [
    "#### d) `insPost`, que acrescenta um novo post à rede social a partir dos parâmetros recebidos e devolve a nova rede social. \n",
    "    \n",
    "O campo `id` devrá ser calculado a partir dos já existentes, por exemplo, se a rede tiver posts com id `p1`, `p2` e `p3`, o novo `id` deverá ser `p4`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "d22b8942",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[{'id': 'p2', 'conteudo': 'a', 'autor': 'a', 'dataCriacao': 'a', 'comentarios': [{'comentario': 'a', 'autorComentario': 'a'}]}, {'id': 'p3', 'conteudo': 'b', 'autor': 'b', 'dataCriacao': 'b', 'comentarios': [{'comentario': 'b', 'autorComentario': 'b'}]}, {'id': 'p4', 'conteudo': 'asd', 'autor': 'a', 'dataCriacao': 'a', 'comentarios': [{'comentario': 'a', 'autorComentario': 'a'}]}]\n"
     ]
    }
   ],
   "source": [
    "def insPost(redeSocial, conteudo, autor, dataCriacao, comentario, autorComentario):\n",
    "    ultimo_id = max(int(post[\"id\"][1:]) for post in redeSocial)\n",
    "    novo_id = f\"p{ultimo_id + 1}\"\n",
    "    novoPost = {\n",
    "        \"id\": novo_id, \n",
    "        \"conteudo\": conteudo,\n",
    "        \"autor\": autor,\n",
    "        \"dataCriacao\": dataCriacao,\n",
    "        \"comentarios\": [\n",
    "            {\n",
    "                \"comentario\": comentario,\n",
    "                \"autorComentario\": autorComentario\n",
    "            }]\n",
    "    }\n",
    "    redeSocial.append(novoPost)\n",
    "    return redeSocial\n",
    "\n",
    "print(insPost(MyFaceBook, input(\"Qual o conteudo do post?\"), input(\"Quem é o autor?\"), input(\"Qual a data?\"), input(\"Qual o comentario?\"), input(\"Quem é o autor do comentario\")))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a3dd764d",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "a5d821ae",
   "metadata": {},
   "source": [
    "#### e)  `remPost`, que remove um post da rede, correspondente ao `id` recebido."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7578c597",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "O post foi removido\n",
      "[{'id': 'p2', 'conteudo': 'a', 'autor': 'a', 'dataCriacao': 'a', 'comentarios': [{'comentario': 'a', 'autorComentario': 'a'}]}]\n"
     ]
    }
   ],
   "source": [
    "def remPost(redeSocial, id):\n",
    "    for i, post in enumerate(redeSocial):\n",
    "        if post[\"id\"] == id:\n",
    "            del redeSocial[i]\n",
    "    print(\"O post foi removido\")\n",
    "    print(redeSocial)\n",
    "\n",
    "remPost(MyFaceBook, input(\"Qual o id?\"))\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1d331877",
   "metadata": {},
   "source": [
    "#### f) `postsPorAutor`, que devolve uma distribuição de posts por autor (à semelhança do que foi feito nas aulas)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "b3ea2bd7",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'a': ['a', 'asd'], 'b': ['b']}\n"
     ]
    }
   ],
   "source": [
    "def postsPorAutor(redeSocial):\n",
    "    distribuicao = {}\n",
    "    for post in redeSocial:\n",
    "        autor = post[\"autor\"]\n",
    "        conteudo = post[\"conteudo\"]\n",
    "        if autor in distribuicao:\n",
    "            distribuicao[autor].append(conteudo)\n",
    "        else:\n",
    "            distribuicao[autor] = [conteudo]\n",
    "    return distribuicao\n",
    "\n",
    "print(postsPorAutor(MyFaceBook))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ec9740e8",
   "metadata": {},
   "source": [
    "#### g) `comentadoPor`, que recebe um autor e devolve a lista de posts comentados por esse autor."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "910c2168",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "a\n",
      "a\n"
     ]
    }
   ],
   "source": [
    "def comentadoPor(redeSocial, autor):\n",
    "    for post in redeSocial:\n",
    "        for comentario in post[\"comentarios\"]:\n",
    "            if comentario[\"autorComentario\"] == autor:\n",
    "                print(f'{comentario[\"comentario\"]}')\n",
    "    return\n",
    "\n",
    "comentadoPor(MyFaceBook, input(\"Qual o nome do Autor:\"))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
