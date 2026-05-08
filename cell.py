import pygame
from constants import BLACK, CELL_SIZE, COLS, ROWS
import random

class Cell:
    """
    Representa uma única célula (um quadradinho) dentro da grade do labirinto.
    Esta classe guarda informações tanto para a parte visual (desenhar paredes) 
    quanto para a lógica matemática do algoritmo (variáveis do A*).
    """
    def __init__(self, col, row):
        # Posição da célula na matriz (coluna X e linha Y)
        self.col = col
        self.row = row
        
        # Dicionário que controla quais paredes estão de pé. 
        # No início, o labirinto é um "grid" denso onde todas as células são fechadas (True).
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
        # Flag usada EXCLUSIVAMENTE pelo gerador de labirinto (Recursive Backtracker).
        # Serve para marcar se o "escavador" já passou por aqui, evitando loops infinitos.
        self.visited = False
        
        # --- Variáveis matemáticas exclusivas para o Algoritmo A* ---
        self.g = 0 # Custo G: Custo real/distância percorrida desde a largada até esta célula
        self.h = 0 # Heurística H: Distância estimada (Manhattan) daqui até o queijo
        self.f = 0 # Custo Total F: A soma de G + H (O A* sempre busca o menor F possível)
        
        # Ponteiro para a célula anterior. Funciona como as "migalhas de pão" de João e Maria:
        # Quando achamos o queijo, usamos esse ponteiro para "andar para trás" e desenhar a linha verde.
        self.previous = None

    def draw(self, surface):
        """
        Responsável por renderizar as paredes da célula na tela do Pygame.
        """
        # Multiplica a coluna e a linha pelo tamanho em pixels (ex: 20px) 
        # para achar a coordenada real (x, y) na janela do jogo.
        x, y = self.col * CELL_SIZE, self.row * CELL_SIZE
        
        # O pygame.draw.line desenha uma linha entre dois pontos (x1,y1) e (x2,y2).
        # Se a parede constar como True no dicionário, a linha preta é desenhada.
        if self.walls['top']:    pygame.draw.line(surface, BLACK, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls['right']:  pygame.draw.line(surface, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls['bottom']: pygame.draw.line(surface, BLACK, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls['left']:   pygame.draw.line(surface, BLACK, (x, y + CELL_SIZE), (x, y), 2)

    def check_neighbors(self, grid):
        """
        Método usado na GERAÇÃO do labirinto (antes do rato começar a andar).
        Ele olha para as 4 direções adjacentes IGNORANDO as paredes, mas 
        respeitando os limites externos da tela (para não dar erro de Index Out of Bounds).
        """
        neighbors = []
        
        # Verifica o vizinho de cima (garantindo que não estamos na linha 0, o teto da tela)
        if self.row > 0: neighbors.append(grid[self.col][self.row - 1])
        # Verifica o da direita (garantindo que não passamos do limite de colunas)
        if self.col < COLS - 1: neighbors.append(grid[self.col + 1][self.row])
        # Verifica o de baixo
        if self.row < ROWS - 1: neighbors.append(grid[self.col][self.row + 1])
        # Verifica o da esquerda
        if self.col > 0: neighbors.append(grid[self.col - 1][self.row])

        # Cria uma nova lista contendo APENAS os vizinhos que ainda não foram visitados
        unvisited = [n for n in neighbors if not n.visited]
        
        # Se houver opções disponíveis, escolhe uma aleatoriamente para o labirinto ser imprevisível.
        # Se não houver (entramos num beco sem saída), retorna None.
        return random.choice(unvisited) if unvisited else None

    def get_valid_neighbors(self, grid):
        """
        Método usado pela INTELIGÊNCIA ARTIFICIAL (Algoritmo A*).
        Diferente da função acima, esta aqui OBRIGATORIAMENTE respeita as paredes. 
        O rato só pode considerar um vizinho como um "passo válido" se a parede entre eles estiver derrubada (False).
        """
        neighbors = []
        
        # Se não tem parede em cima, o caminho para o Norte é válido
        if not self.walls['top']:    neighbors.append(grid[self.col][self.row - 1])
        # Se não tem parede na direita, o caminho para o Leste é válido
        if not self.walls['right']:  neighbors.append(grid[self.col + 1][self.row])
        # O mesmo para o Sul
        if not self.walls['bottom']: neighbors.append(grid[self.col][self.row + 1])
        # O mesmo para o Oeste
        if not self.walls['left']:   neighbors.append(grid[self.col - 1][self.row])
        
        return neighbors