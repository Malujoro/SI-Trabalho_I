import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from random import randint
from math import sqrt, atan2, degrees

# largura e altura da tela, respectivamente
tamanho_tela = (1000, 1000)
raio = 100
quant_obstaculos = 5

cores = ["blue", "red", "purple", "cyan", "orange", "green", "magenta"]
cor_atual = 0

def desenhar_circulo(ax, coord, raio, color):
    ax.add_patch(Circle(coord, raio, color=color))

def desenhar_arco(ax, centro, raio, p1, p2, color="black"):
    x0, y0 = centro

    # Ângulos em radianos para graus
    ang1 = degrees(atan2(p1[1] - y0, p1[0] - x0)) % 360
    ang2 = degrees(atan2(p2[1] - y0, p2[0] - x0)) % 360

    # Calcula a diferença mínima entre ângulos (arco menor)
    diff = (ang2 - ang1) % 360
    if diff > 180:   # Pega sempre o menor arco
        ang1, ang2 = ang2, ang1

    # Cria arco apenas nesse intervalo
    arco = Arc((x0, y0), 2 * raio, 2 * raio, angle=0,
               theta1=ang1, theta2=ang2, color=color, lw=2)

    ax.add_patch(arco)

def desenhar_aresta(ax, pt1, pt2, color=None):
    if (not color):
        global cor_atual
        color = cores[cor_atual % len(cores)]
        cor_atual += 1

    x1, y1 = pt1["ponto"]
    x2, y2 = pt2["ponto"]

    if (pt1["centro"] == pt2["centro"]):
        # Desenha o arco
        desenhar_arco(ax, pt1["centro"], raio,
                      pt1["ponto"], pt2["ponto"], color=color)
    else:
        # Desenha a reta
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

def tupla_para_aresta(tupla):
    return (tupla[0]["ponto"], tupla[1]["ponto"])

def existe_coord(lista, aresta):
    for tupla in lista:
        aresta_base = tupla_para_aresta(aresta)
        aresta_tupla1 = tupla_para_aresta(tupla)
        aresta_tupla2 = tupla_para_aresta((tupla[0], tupla[1]))

        if (aresta_base == aresta_tupla1 or aresta_base == aresta_tupla2):
            return True

    return False

def busca_profundidade(plt, ax, p1, p2, arestas, visitados=[]):

    if (existe_coord(arestas, (p1, p2))):
        desenhar_aresta(ax, p1, p2)
        return True

    visitados.append((p1, p2))

    resultado = False
    for aresta in arestas:

        if (not existe_coord(visitados, aresta)):
            aresta_tupla = tupla_para_aresta(aresta)

            if (p1["ponto"] in aresta_tupla):
                visitados.append(aresta)

                if (p1["ponto"] == aresta_tupla[0]):
                    prox_ponto = aresta[1]

                elif (p1["ponto"] == aresta_tupla[1]):
                    prox_ponto = aresta[0]

                resultado = busca_profundidade(
                    plt, ax, prox_ponto, p2, arestas, visitados)

            if (resultado):
                desenhar_aresta(ax, aresta[0], aresta[1])
                return resultado

    return False

def criar_dicionario(ponto, centro):
    return {"ponto": ponto, "centro": centro}


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
            desenhar_circulo(ax, (larg, alt), raio, "lightgray")
            plt.draw()
            # plt.pause(0.5)

    print(f"Foram inseridos {len(obstaculos)} obstáculos")

    arestas = []

    # ================== Plotagem dos pontos ==================
    pontos_obstaculos = []
    for it, (x, y) in enumerate(obstaculos):
        # Ponto superior
        pontos_obstaculos.append(criar_dicionario((x, y - raio), (x, y)))
        # Ponto esquerda
        pontos_obstaculos.append(criar_dicionario((x - raio, y), (x, y)))
        # Ponto inferior
        pontos_obstaculos.append(criar_dicionario((x, y + raio), (x, y)))
        # Ponto direita
        pontos_obstaculos.append(criar_dicionario((x + raio, y), (x, y)))

        # ================== Plotagem das "arestas internas" ==================
        # Posição inicial dos pontos (Ex: 0, 4, 8)
        inicio = it * 4
        tam = len(pontos_obstaculos)
        pos = inicio
        for coord_dict in pontos_obstaculos[inicio:]:
            coord = coord_dict["ponto"]
            desenhar_circulo(ax, coord, 5, "black")
            # Aresta interna do obstáculo
            if (pos + 1 < tam):
                arestas.append(
                    (pontos_obstaculos[pos], pontos_obstaculos[pos + 1]))

                # desenhar_aresta(
                #     ax, pontos_obstaculos[pos], pontos_obstaculos[pos + 1], "red")
            else:
                arestas.append(
                    (pontos_obstaculos[pos], pontos_obstaculos[inicio]))

                # desenhar_aresta(
                #     ax, pontos_obstaculos[pos], pontos_obstaculos[inicio], "red")
            pos += 1

        print((x, y), end=" ")
        print((pontos_obstaculos[it * 4:]))

    # Adição do ponto inicial
    ponto_inicial_dict = criar_dicionario(ponto_inicial, ponto_inicial)
    pontos_obstaculos.append(ponto_inicial_dict)
    # Adição do ponto final
    ponto_final_dict = criar_dicionario(ponto_final, ponto_final)
    pontos_obstaculos.append(ponto_final_dict)

    # ================== Plotagem das arestas ==================
    for i in range(len(pontos_obstaculos)):
        ponto_i = pontos_obstaculos[i]
        pt1 = ponto_i["ponto"]
        for j in range(i + 1, len(pontos_obstaculos)):
            ponto_j = pontos_obstaculos[j]
            pt2 = ponto_j["ponto"]
            colidiu = False
            for obst in obstaculos:
                if (colide_segmento_circulo(pt1, pt2, obst, raio)):
                    colidiu = True
                    break
            if (not colidiu):
                # 'lightgray', 'gainsboro', 'silver'
                # 'beige', 'linen', 'ivory'
                desenhar_aresta(ax, ponto_i, ponto_j, "lightgray")
                arestas.append((ponto_i, ponto_j))

    if (busca_profundidade(plt, ax, ponto_inicial_dict, ponto_final_dict, arestas)):
        print("Encontrou caminho")
    else:
        print("Não encontrou caminho")

    plt.ioff()
    plt.show()


# Exemplo de uso:
if __name__ == "__main__":
    mostrar_tela(tamanho_tela[0], tamanho_tela[1], raio, quant_obstaculos)
