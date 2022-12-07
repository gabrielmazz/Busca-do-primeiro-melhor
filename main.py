# Algoritmo da busca do primeiro melhor
# Inteligencia Artificial - Professor Andre Luiz Brun
# UNIOESTE - Universidade Estadual do Oeste do Paraná
# Nomes: Gabriel Mazzuco, Rodrigo Brickmann, Guilherme Correia

# Sumário:
    # Matriz_cenario:
        # 0  = caminho livre
        # -1 = barcos
        # 15 = luffy
        # 99 = one_piece
        # 1000 = one_piece foi encontrado
        
    # Matriz_valores:
        # 700.0 = barcos
        # 800.0 = caminhos já percorridos
        # 999.9 = void do mapa -> "valor teorico que não aparece de fato no mapa"
        
import numpy as np
import math
import random
import os
import sys

# Define o personagem, aleatorizando a sua posição dentro do grid
class Luffy:
    def __init__(self, x, y):
        self.posicaoX = random.randint(0, x-1)
        self.posicaoY = random.randint(0, y-1)

# Define o tesouro, aleatorizando a sua posição dentro do grid        
class OnePiece:
    def __init__(self, x, y):
        self.posicaoX = random.randint(0, x-1)
        self.posicaoY = random.randint(0, y-1)
       
# Define os barcos, aleatorizando a sua posição dentro do grid, e dentro dela, terá a criação de
# quantos navios terá, verificando a dificuldade estabelecida no algoritmo 
class Navio:
    def __init__(self, x, y, matriz_cenario, dificuldade):
        for i in range(Navio.Barcos()):
            matriz_cenario[random.randint(0, x-1), random.randint(0, y-1)] = -1
            
        
    # Define quantos barcos apareceram no mapa, para aumentar a dificuldade, é so mudar o valor da divisão
    def Barcos():
        aux = x * y / Navio.trueDificuldade()
        aux = math.ceil(aux) 
        return aux 
    
    def trueDificuldade():
        if(dificuldade == 1):
            return 8
            
        elif(dificuldade == 2):
            return 4
            
        elif(dificuldade == 3):
            return 2
            
        elif(dificuldade == 4):
            return 1
  
# Usando a trigonometria, será criado a matriz estimativa, aonde o personagem verificara qual a melhor
# posição que ele podera andar  
def calculaEstimativa(posicaoX, posicaoY):
    if (matriz[posicaoX, posicaoY] == -1):
        return -1
    else:
        medida1 = abs(posicaoX - tesouro.posicaoX)
        medida2 = abs(posicaoY - tesouro.posicaoY)
        medida3 = (pow(medida1, 2)) + (pow(medida2, 2))
        estimativa = math.sqrt(medida3)
        return estimativa
 
# Ordena os dois vetores com base no primeiro, já que apenas é possivel ordenar os valores, é estabelecido
# um index que permitira ordenar a fila de posições. Com base na ordenação, o personagem fara o seu movimento   
def ordena(fila_valores, fila_posicoes):
    #https://pt.stackoverflow.com/questions/507769/ordenar-duas-listas-com-base-na-ordem-da-primeira
    x = fila_valores
    y = fila_posicoes

    # Ordene os índices em vez dos elementos em si
    indices = list(range(len(x)))
    
    # Ordene os índices com relação ao seu respectivo valor em x
    indices.sort(key=lambda i: x[i]) 

    # Crie as listas baseado na ordem dos índices
    new_x = [x[i] for i in indices]
    new_y = [y[i] for i in indices]

    return new_x, new_y

# Define as posições possiveis que o personagem pode andar, salvando as posições de cima, baixo, esquerda e direta
def posicaoPersonagem(fila_posicoes, posicaoX, posicaoY):
    aux = posicaoX - 1, posicaoY 
    fila_posicoes.append(aux) # Cima
            
    aux = posicaoX + 1, posicaoY
    fila_posicoes.append(aux) # Baixo
            
    aux = posicaoX, posicaoY - 1
    fila_posicoes.append(aux) # Esquerda
            
    aux = posicaoX, posicaoY + 1
    fila_posicoes.append(aux) # Direita

    return fila_posicoes

# Definira a fila de valores com base na matriz de valores, com a posição alcançada dentro da posicaoPersonagem()
# dentro ocorrendo uma verificação se o personagem está na borda do void
def movimentacaoPersonagem(matriz, fila_posicoes, fila_valores, posicaoX, posicaoY):
    # Cima
    if(fila_posicoes[0][0] == -1):
        aux = 999.9
        fila_valores.append(aux)
    else:
        aux = matriz[posicaoX - 1, posicaoY]
        fila_valores.append(aux)
    
    # Baixo
    if(fila_posicoes[1][0] == x):
        aux = 999.9
        fila_valores.append(aux)	
    else:
        aux = matriz[posicaoX + 1, posicaoY]
        fila_valores.append(aux)

    # Esquerda
    if(fila_posicoes[2][1] == -1):
        aux = 999.9
        fila_valores.append(aux)
    else:
        aux = matriz[posicaoX, posicaoY - 1]
        fila_valores.append(aux)
       
    # Direita   
    if(fila_posicoes[3][1] == y):
        aux = 999.9
        fila_valores.append(aux)
    else:
        aux = matriz[posicaoX, posicaoY + 1]
        fila_valores.append(aux) 
    
    return fila_valores           

# Verificação se o personagem está preso, no caso se os valores estão muito descrepantes, impossibilitando do
# personagem de andar para qualquer lado
def verificaObstrucao(fila_valores):
    if((fila_valores[3] == 700.0) or (fila_valores[3] == 800.0) or (fila_valores[3] == 999.9)):
        if((fila_valores[2] == 700.0) or (fila_valores[2] == 800.0) or (fila_valores[2] == 999.9)):
            if((fila_valores[1] == 700.0) or (fila_valores[1] == 800.0) or (fila_valores[1] == 999.9)):
                if((fila_valores[0] == 700.0) or (fila_valores[0] == 800.0) or (fila_valores[0] == 999.9)):
                    return True
    else:
        return False
  
# Função para printar as informações necessárias, a cada iteração que será feita  
def printaTerminal(iteracao, luffy, one_piece, posicaoX, posicaoY, fila_valores, fila_posicoes, matriz, matriz_cenario):
    
    print('Iteração: ', iteracao)
    print('Posição inicial do Personagem: ', luffy)
    print('Posição agora do personagem: ', posicaoX, posicaoY)
    print('Tesouro: ' , one_piece)
    print('Fila com valores: ', fila_valores)
    print('Fila com as posições: ', fila_posicoes)
    print('\n')
    print(matriz)
    print('\n')
    print(matriz_cenario)
    print("--------------------------------------------------------------")
    print('\n')

# Começa o programa
if __name__ == '__main__':

    # Define o tamanho da matriz, podendo ser de várias formas
    print("Busca do primeiro melhor, determine a matriz grid:\n")
    x = int(input("Determina o x da matriz: "))
    y = int(input("Determina o y da matriz: "))
    
    os.system('clear')
    
    # Seleção da dificuldade do jogo
    while True:
        print('''Dificuldade do jogo: 
          1 - Fácil
          2 - Médio
          3 - Díficil
          4 - Muito Díficil''')
        
        dificuldade = (int(input('Escolha uma opção: ')))
        
        if((dificuldade > 4) or (dificuldade < 1)):
            print("Opção inválida, escolha novamente")
        else:
            break
    
    os.system('clear')

    # Cria a matriz que será o cenario do jogo
    matriz_cenario = (np.zeros((x,y)))

    # Cria as classes da matrizes
    personagem = Luffy(x, y)
    tesouro = OnePiece(x, y)
    navio = Navio(x, y, matriz_cenario, dificuldade)

    os.system('clear') or None

    # Cria a matriz com valore em zero
    matriz = np.zeros((x,y), dtype=np.float64)

    os.system('clear') or None

    # Define a matriz com as estimativas inicias, mostrando apenas 2 valores
    # nas casa decimais
    for i in range(x):
        for j in range(y):
            matriz[i, j] = "{:.2f}" .format(calculaEstimativa(i, j))
    
    matriz_cenario[personagem.posicaoX, personagem.posicaoY] = 15
    matriz_cenario[tesouro.posicaoX, tesouro.posicaoY] = 99
    
    # Adiciona os barcos nas posições dentro da matriz de estimativas
    for i in range(x):
        for j in range(y):
            if(matriz_cenario[i, j] == -1):
                matriz[i, j] = 700.0

    # Variavel de controle apenas para ver qual interação está sendo feita
    iteracao = 0

    # Inicia de fato o programa
    # Fila de posição do caminho
    fila_valores = []
    fila_posicoes = []
    caminho = []
    
    # Aonde o personagem começa
    luffy = personagem.posicaoX, personagem.posicaoY
    one_piece = tesouro.posicaoX, tesouro.posicaoY
    
    luffy_inicial = luffy

    # Verifica se o tesouro foi aleatorizado em cima do personagem
    if(luffy == one_piece):
        print('O One Piece estava do seu lado o tempo todo')
        exit() # Sai direto do programa
    else:
        while (luffy != one_piece):
            iteracao = iteracao + 1
            
            # Pega a posição do personagem e o valor que custara está movimentação 
            posicaoPersonagem(fila_posicoes, personagem.posicaoX, personagem.posicaoY)
            movimentacaoPersonagem(matriz, fila_posicoes, fila_valores, personagem.posicaoX, personagem.posicaoY)
            
            # Ordena os dois vetores com base no primeiro
            fila_valores, fila_posicoes = ordena(fila_valores, fila_posicoes)
            
            # Testa se a fila esta vazia
            if (fila_posicoes == []):
                break
            
            # Primeiro print, aonde o luffy começara e aonde o one piece está
            printaTerminal(iteracao, luffy_inicial, one_piece, personagem.posicaoX, personagem.posicaoY, fila_valores, fila_posicoes, matriz, matriz_cenario)
            
            # Adiciona o caminho percorrido
            caminho.append(luffy)
            
            # Atribui um valor para o boneco não retornar
            matriz[personagem.posicaoX, personagem.posicaoY] = 800.0
            
            # Atribui a proxima posição nas coordenadas
            personagem.posicaoX = fila_posicoes[0][0]
            personagem.posicaoY = fila_posicoes[0][1]
            luffy = personagem.posicaoX, personagem.posicaoY
            
            # Move o personagem para a nova posição
            matriz_cenario[personagem.posicaoX, personagem.posicaoY] = 15
            
            if(verificaObstrucao(fila_valores) == True):
                print('Luffy se perdeu e não achou os Road Poneglyph!!!')
                printaTerminal(iteracao, luffy_inicial, one_piece, personagem.posicaoX, personagem.posicaoY, fila_valores, fila_posicoes, matriz, matriz_cenario)
                exit()
            
            # Zera as filas para não ter lixo no buffer
            fila_posicoes.clear()
            fila_valores.clear()
            
    if(luffy == one_piece):
        # Adiciona um novo valor apenas se o one piece for encontrado, para diferenciar apenas
        matriz_cenario[tesouro.posicaoX, tesouro.posicaoY] = 1000
        print("\n\nO luffy finalmente encontrou o One Piece, seu caminho foi esse: ", caminho)
        printaTerminal(iteracao, luffy_inicial, one_piece, personagem.posicaoX, personagem.posicaoY, fila_valores, fila_posicoes, matriz, matriz_cenario)
        