# 1 entrega SI (20/04)
# - Plotagem com ponto inicial e final (fixos/dinâmico) (Ex: (0,0) (1000, 1000))

# Parâmetros
# - Quantidade de obstáculos
# - Obstáculos não podem colidir (sobreposição) entre si
# - Tamanho do raio dos obstáculos (podem ser iguais)
# * Posição dos obstáculos (deve ser aleatório e dentro do intervalo)

# NÃO DEVE FAZER ❌
# - Arestas
# - Com matriz

# Sugestão
# - Lista com as coordenadas do obstáculo

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from random import randint
from math import sqrt

# largura e altura da tela, respectivamente
tamanho_tela = (1000, 1000)
raio = 30
quant_obstaculos = 40

def desenhar_circulo(ax, coord, raio, color):
    ax.add_patch(Circle(coord, raio, color=color))

def mostrar_tela(largura, altura, raio, quant_obstaculos):
    # Modo interativo (para ver a geração de cada obstáculo)
    plt.ion()

    # Tamanho em polegadas
    polegadas = 100
    fig, ax = plt.subplots(figsize=(largura / polegadas, altura / polegadas), dpi=polegadas)
    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)

    # Inverte o eixo Y (para o 0,0 ser o canto superior esquerdo)
    ax.invert_yaxis()

    # Ponto Inicial
    desenhar_circulo(ax, (0, 0), 10, "red")

    # Ponto Final
    desenhar_circulo(ax, (largura, altura), 10, "blue")

    ax.set_title("Busca com obstáculos")

    # Obstaculos
    obstaculos = []

    cont = 0
    quant = 0
    it = 0
    while cont < 10_000 and quant < quant_obstaculos:
        it += 1
        larg = randint(raio, largura - raio)
        alt = randint(raio, altura - raio)

        print(larg, alt)

        # X = largura, Y = altura
        for (x, y) in obstaculos:
            coord_x = pow(x - larg, 2)
            coord_y = pow(y - alt, 2)
            result = sqrt(coord_x + coord_y)
            if (result <= (2 * raio)):
                print(f"Colidiu {it}")
                cont += 1
                break
        else:
            cont = 0
            quant += 1
            print(f"Entrou else {it}")
            obstaculos.append((larg, alt))
            desenhar_circulo(ax, (larg, alt), raio, "green")
            plt.draw()
            plt.pause(0.5)

    print(f"Foram inseridos {quant} obstáculos")
    plt.ioff()
    plt.show()


# Exemplo de uso:
if __name__ == "__main__":
    mostrar_tela(tamanho_tela[0], tamanho_tela[1], raio, quant_obstaculos)
