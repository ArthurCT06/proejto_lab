import pygame

# ==========================================
# CONFIGURAÇÕES GERAIS DA JANELA E MATRIZ
# ==========================================

# Dimensões totais da janela do jogo em pixels (Largura e Altura)
WIDTH, HEIGHT = 600, 600

# Define a quantidade de colunas e linhas da nossa matriz (labirinto).
# Como temos 20x20, o nosso algoritmo A* terá que lidar com 400 células no total.
COLS, ROWS = 20, 20

# Calcula o tamanho exato (em pixels) de cada quadradinho na tela.
# O uso de '//' (divisão inteira no Python) é proposital e muito importante aqui:
# Ele garante que o resultado seja um número inteiro (ex: 600 // 20 = 30 pixels), 
# evitando números quebrados (float) que podem causar falhas ou borrões de renderização no Pygame.
CELL_SIZE = WIDTH // COLS

# ==========================================
# PALETA DE CORES (Padrão RGB - Red, Green, Blue)
# ==========================================
# No motor gráfico do Pygame, as cores são representadas por tuplas numéricas.
# Cada canal de cor (Vermelho, Verde e Azul) recebe uma intensidade de 0 a 255.

WHITE  = (255, 255, 255) # Fundo da tela (usado a cada frame para "limpar" o frame anterior)
BLACK  = (0, 0, 0)       # Cor das linhas que representam as paredes intransponíveis

GREEN  = (50, 205, 50)   # Usado para pintar o rastro do caminho final descoberto pela Inteligência Artificial
BLUE   = (65, 105, 225)  # Representa o nosso Rato (o agente que faz a busca no labirinto)
YELLOW = (255, 215, 0)   # Representa o nosso Queijo (o nó/célula objetivo do algoritmo)
GRAY   = (200, 200, 200) # Cor extra de apoio