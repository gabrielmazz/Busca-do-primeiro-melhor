import numpy as np
import math
import random
import os

class Luffy:
    def __init__(self, x, y):
        self.posicaoX = random.randint(0, x-1)
        self.posicaoY = random.randint(0, y-1)
        
class OnePiece:
    def __init__(self, x, y):
        self.posicaoX = random.randint(0, x-1)
        self.posicaoY = random.randint(0, y-1)
        
class Navio:
    def __init__(self, x, y, matriz_cenario):
        for i in range(Navio.Barcos()):
            matriz_cenario[random.randint(0, x-1), random.randint(0, y-1)] = -1
        
    # Define quantos barcos apareceram no mapa
    def Barcos():
        aux = x * y / 8 
        aux = math.ceil(aux) 
        return aux 
    
def calculaEstimativa(posicaoX, posicaoY):
    if (matriz[posicaoX, posicaoY] == -1):
        return -1
    else:
        medida1 = abs(posicaoX - tesouro.posicaoX)
        medida2 = abs(posicaoY - tesouro.posicaoY)
        medida3 = (pow(medida1, 2)) + (pow(medida2, 2))
        estimativa = math.sqrt(medida3)
        return estimativa

def posicaoPersonagem(x, y, fila, posicaoX, posicaoY):    
    aux = posicaoX - 1, posicaoY 
    if(posicaoX <= -1):
        fila.append("Invalido")
    else:
        fila.append(aux) # Esquerda
            
    aux = posicaoX + 1, posicaoY
    if(posicaoX >= x+1):
        fila.append("Invalido")
    else:
        fila.append(aux) # Direita
            
    aux = posicaoX, posicaoY - 1
    if(posicaoY <= -1):
        fila.append("Invalido")
    else:
        fila.append(aux) # Cima
            
    aux = posicaoX, posicaoY + 1
    if(posicaoY >= y+1):
        fila.append("Invalido")
    else:
        fila.append(aux) # Baixo
    
    print(fila)
    return fila

def custoMovimentacao(fila, fila_aux, matriz):
    for i in range(len(fila)):
        aux = matriz[fila[i][0], fila[i][1]]
        fila_aux.append(aux)
        
    return fila_aux

def escreveArquivo(x, y, matriz, matriz_cenario, caminho, personagemX, personagemY, tesouroX, tesouroY):
    arquivo = open("resposta.txt", "w")
    
    # Posição do personagem/tesouro
    arquivo.write("Posição do Personagem: "+ str(personagemX) + " " + str(personagemY) + "\n")
    arquivo.write("Posição do Tesouro: "+ str(tesouroX) + " " + str(tesouroY) + "\n\n")
    
    # Matriz de custo
    arquivo.write("Matriz de Custo: \n")
    for i in range(x):
        for j in range(y):
            arquivo.write(str(matriz[i, j]))
            arquivo.write(" ")
        arquivo.write("\n")

    arquivo.write("\n\n")

    # Matriz de cenario
    arquivo.write("Matriz de Cenário: \n")
    for i in range(x+2):
        for j in range(y+2):
            arquivo.write(str(matriz_cenario[i, j]))
            arquivo.write(" ")
        arquivo.write("\n")
            
    arquivo.write("\nCaminho: " + str(caminho))
    
    arquivo.close()

# Começa o programa
if __name__ == '__main__':

    # Define o tamanho da matriz, podendo ser de várias formas
    x = int(input("Determina o x da matriz: "))
    y = int(input("Determina o y da matriz: "))

    # Cria a matriz que será o cenario do jogo
    matriz_cenario = np.zeros((x,y))

    # Cria as classes da matrizes
    personagem = Luffy(x, y)
    tesouro = OnePiece(x, y)
    navio = Navio(x, y, matriz_cenario)

    # Cria o void do mapa com -1
    matriz_cenario = np.pad(matriz_cenario, pad_width=1, mode='constant', constant_values=-1)

    os.system('clear') or None

    # Cria a matriz com valore em zero
    matriz = np.zeros((x,y), dtype=np.float64)

    os.system('clear') or None

    # Define a matriz com as estimativas inicias, mostrando apenas 2 valores
    # nas casa decimais
    for i in range(x):
        for j in range(y):
            matriz[i, j] = "{:.2f}" .format(calculaEstimativa(i, j))
            
    matriz_cenario[personagem.posicaoX, personagem.posicaoY] = 10
    matriz_cenario[tesouro.posicaoX, tesouro.posicaoY] = 100

    # Inicia de fato o programa
    # Fila de posição do caminho
    fila = []
    fila_aux = []
    
    # Caminho que o personagem ira percorrer
    caminho = []
    
    # Aonde o personagem começa
    luffy = personagem.posicaoX, personagem.posicaoY
    one_piece = tesouro.posicaoX, tesouro.posicaoY

    # Laço para encontrar o One Piece
    if(luffy == one_piece):
        print('O One Piece estava do seu lado o tempo todo')
    else:
        while (luffy != one_piece):
            
            # Pega a posição do personagem
            posicaoPersonagem(x ,y, fila, personagem.posicaoX, personagem.posicaoY)

            # Usa a posição do personagem para pegar na matriz de custo
            custoMovimentacao(fila, fila_aux, matriz)
            
            # Ordena a lista de numeros
            fila_aux = sorted(fila_aux)
            
            # Testa se a fila esta vazia
            if (fila == []):
                break
            
            # Atribui a nova posicao para o personagem
            personagem.posicaoX = fila[0][0]
            personagem.posicaoY = fila[0][1]
            
            #print(personagem.posicaoX, personagem.posicaoY)
            
            # Atribui um valor que nao podera voltar
            matriz[personagem.posicaoX, personagem.posicaoY] = 999
            
            # Recebe a nova posição para as comparações
            luffy = personagem.posicaoX, personagem.posicaoY
            
            # Adiciona o caminho que esta sendo percorrido
            caminho.append(fila[0])
            #print(caminho)
                
            #variavel += 1    
            fila.clear()

            
    escreveArquivo(x, y, matriz, matriz_cenario, caminho,
                   personagem.posicaoX, personagem.posicaoY,
                   tesouro.posicaoX, tesouro.posicaoY)


    #print('Perosnagem: ', personagem.posicaoX, personagem.posicaoY)
    #print('Tesouro: ' , tesouro.posicaoX, tesouro.posicaoY)
    #print('\n')
    #print(matriz)
    #print('\n')
    #print(matriz_cenario)
    #print('\n')
    
    #print(fila)
    #print(fila[3])
  