TPC1 Duarte Matos; A110102;
<img width="2316" height="3088" alt="image" src="https://github.com/user-attachments/assets/0046bd0c-37a9-416c-a565-7e7f9aba08f9" />
"### TPC4: Aplicação para Gerir um Cinema

Suponha que está a desenvolver uma aplicacão para gestão de um conjunto de salas de cinema de um centro comercial. 
Nesse centro comercial existem algumas salas de cinema (que poderão estar a exibir filmes ou não), cada sala tem uma determinada 
lotação, uma lista com a referência dos bilhetes vendidos (lugares ocupados; cada lugar é identificado por um número inteiro), e cada sala tem um filme associado.

Considera a seguinte sugestão para o modelo dos cinemas:
```
Cinema = [Sala]
Sala = [nlugares, Vendidos, filme]
nlugares = Int
filme = String 
Vendidos = [Int]
```
  
Que poderá ser usado num programa da seguinte forma:
```
sala1 = (150, [], "Twilight")
sala2 = (200, [], "Hannibal")
cinema1 = []
...
cinema1 = inserirSala(cinema1,sala1)
cinema1 = inserirSala(cinema1,sala2)
...
listar(cinema1)
...

if(disponivel(cinema1, "Twilight", 17 )):
  cinema1 = vendebilhete(cinema1, "Twilight", 17 )
...
listardisponibilidades(cinema1)
...
```

Especifique as funções utilizadas no exemplo:

1. `listar( cinema )` - que lista no monitor todos os filmes que estão em exibição nas salas do cinema passado como argumento;
2. `disponivel( cinema, filme, lugar )` - que dá como resultado **False** se o lugar lugar já estiver ocupado na sala onde o filme está a ser exibido e dará como resultado **True** se o inverso acontecer;
3. `vendebilhete( cinema, filme, lugar )` - que dá como resultado um novo cinema resultante de acrescentar o lugar à lista dos lugares ocupados, na sala onde está a ser exibido o filme;
4. `listardisponibilidades( cinema )` - que, para um dado cinema, lista no monitor para cada sala, o filme que está a ser exibido e o total de lugares disponíveis nessa sala (número de lugares na sala menos o número de lugares ocupados);"
<img width="1861" height="1156" alt="cin1 1" src="https://github.com/user-attachments/assets/f76a49c0-9392-4060-9ecd-712cff32d784" />
<img width="1842" height="1127" alt="cin1 2" src="https://github.com/user-attachments/assets/67247562-14cf-4de3-bf67-9837b3fe3e5a" />
<img width="1853" height="1117" alt="cin1 3" src="https://github.com/user-attachments/assets/dbe900a1-799c-4217-99fe-ff194de41c7a" />



5. `inserirSala( cinema, sala )` - que acrescenta uma sala nova a um cinema (devendo verificar se a sala já existe);

