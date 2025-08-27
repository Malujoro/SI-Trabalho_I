import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from random import randint
from math import sqrt

# largura e altura da tela, respectivamente
tamanho_tela = (1000, 1000)
raio = 100
quant_obstaculos = 5

def desenhar_circulo(ax, coord, raio, color):
    ax.add_patch(Circle(coord, raio, color=color))

def desenhar_aresta(ax, pt1, pt2, color="yellow"):
    x1, y1 = pt1
    x2, y2 = pt2
    ax.plot([x1, x2], [y1, y2], color=color)

# Função para verificar se uma aresta passa por dentro de um círculo
def colide_segmento_circulo(p1, p2, centro, raio):
    x1, y1 = p1
    x2, y2 = p2
    xc, yc = centro

    dx = x2 - x1
    dy = y2 - y1
    fx = xc - x1
    fy = yc - y1

    # Projeção do centro na reta
    t = (fx * dx + fy * dy) / (dx * dx + dy * dy)

    if t < 0:   # Círculo "antes" de p1
        dist = sqrt((xc - x1) ** 2 + (yc - y1) ** 2)
    elif t > 1:  # Círculo "depois" de p2
        dist = sqrt((xc - x2) ** 2 + (yc - y2) ** 2)
    else:       # Círculo "dentro" da reta
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        dist = sqrt((xc - proj_x) ** 2 + (yc - proj_y) ** 2)

    return dist < raio

def busca_profundidade(plt, ax, p1, p2, arestas, visitados=[]):

    if ((p1, p2) in arestas or (p2, p1) in arestas):
        desenhar_aresta(ax, p1, p2, color="black")
        return True

    visitados.append((p1, p2))
    # input(f"{p1}, {p2}")

    resultado = False
    for aresta in arestas:
        # print(f"{visitados}")
        # print(f"{aresta} not in |  and ({aresta[1]}, {aresta[0]}) not in | ")

        # input(
        #     f"{aresta not in visitados and (aresta[1], aresta[0]) not in visitados}")

        # print()

        if (aresta not in visitados and (aresta[1], aresta[0]) not in visitados):
            if (p1 in aresta):

                # desenhar_aresta(ax, aresta[0], aresta[1], color="blue")
                visitados.append(aresta)

                if (p1 == aresta[0]):
                    # print(f"É aresta[0]")

                    visitados.append(aresta)

                    resultado = busca_profundidade(
                        plt, ax, aresta[1], p2, arestas, visitados)
                elif (p1 == aresta[1]):
                    # print(f"É aresta[1]")

                    resultado = busca_profundidade(
                        plt, ax, aresta[0], p2, arestas, visitados)

            if (resultado):
                desenhar_aresta(ax, aresta[0], aresta[1], color="black")
                return resultado

    return False


def mostrar_tela(largura, altura, raio, quant_obstaculos):
    # Modo interativo (para ver a geração de cada obstáculo)
    plt.ion()

    # Tamanho em polegadas
    polegadas = 100
    fig, ax = plt.subplots(
        figsize=(largura / polegadas, altura / polegadas), dpi=polegadas)
    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)

    # Inverte o eixo Y (para o 0,0 ser o canto superior esquerdo)
    ax.invert_yaxis()

    # Ponto Inicial
    ponto_inicial = (0, 0)
    desenhar_circulo(ax, ponto_inicial, 10, "red")

    # Ponto Final
    ponto_final = (largura, altura)
    desenhar_circulo(ax, ponto_final, 10, "blue")

    ax.set_title("Busca com obstáculos")

    # Obstaculos
    obstaculos = []

    # ================== Plotagem dos obstáculos ==================
    cont = 0
    it = 0
    while cont < 10_000 and len(obstaculos) < quant_obstaculos:
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
            print(f"Entrou else {it}")
            obstaculos.append((larg, alt))
            desenhar_circulo(ax, (larg, alt), raio, "green")
            plt.draw()
            # plt.pause(0.5)

    print(f"Foram inseridos {len(obstaculos)} obstáculos")

    arestas = []

    # ================== Plotagem dos pontos ==================
    pontos_obstaculos = []
    for it, (x, y) in enumerate(obstaculos):
        # Ponto superior
        pontos_obstaculos.append((x, y - raio))
        # Ponto esquerda
        pontos_obstaculos.append((x - raio, y))
        # Ponto inferior
        pontos_obstaculos.append((x, y + raio))
        # Ponto direita
        pontos_obstaculos.append((x + raio, y))

        # ================== Plotagem das "arestas internas" ==================
        # Posição inicial dos pontos (Ex: 0, 4, 8)
        inicio = it * 4
        tam = len(pontos_obstaculos)
        pos = inicio
        for coord in pontos_obstaculos[inicio:]:
            desenhar_circulo(ax, coord, 5, "black")
            if (pos + 1 < tam):
                arestas.append(
                    (pontos_obstaculos[pos], pontos_obstaculos[pos + 1]))

                desenhar_aresta(
                    ax, pontos_obstaculos[pos], pontos_obstaculos[pos + 1], "red")
            else:
                arestas.append(
                    (pontos_obstaculos[pos], pontos_obstaculos[inicio]))

                desenhar_aresta(
                    ax, pontos_obstaculos[pos], pontos_obstaculos[inicio], "red")
            pos += 1

        print((x, y), end=" ")
        print((pontos_obstaculos[it * 4:]))

    # Adição do ponto inicial
    pontos_obstaculos.append((0, 0))
    # Adição do ponto final
    pontos_obstaculos.append((largura, altura))

    # ================== Plotagem das arestas ==================
    for i in range(len(pontos_obstaculos)):
        pt1 = pontos_obstaculos[i]
        for j in range(i + 1, len(pontos_obstaculos)):
            pt2 = pontos_obstaculos[j]
            colidiu = False
            for obst in obstaculos:
                if (colide_segmento_circulo(pt1, pt2, obst, raio)):
                    colidiu = True
                    break
            if (not colidiu):
                desenhar_aresta(ax, pt1, pt2)
                arestas.append((pt1, pt2))

    if (busca_profundidade(plt, ax, ponto_inicial, ponto_final, arestas)):
        print("Encontrou caminho")
    else:
        print("Não encontrou caminho")

    plt.ioff()
    plt.show()


# Exemplo de uso:
if __name__ == "__main__":
    mostrar_tela(tamanho_tela[0], tamanho_tela[1], raio, quant_obstaculos)
