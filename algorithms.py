import random
from cell import Cell
from constants import COLS, ROWS

def remove_walls(a, b):
    """
    Derruba as paredes compartilhadas entre duas células adjacentes (a e b).
    Calcula a diferença entre as coordenadas (dx, dy) para descobrir qual a 
    posição relativa entre elas (ex: se 'a' está à direita de 'b').
    """
    dx, dy = a.col - b.col, a.row - b.row
    
    # Eixo X (Movimento Horizontal)
    if dx == 1:  # 'a' está à direita de 'b'. Quebra a esquerda de 'a' e a direita de 'b'.
        a.walls['left'], b.walls['right'] = False, False
    if dx == -1: # 'a' está à esquerda de 'b'.
        a.walls['right'], b.walls['left'] = False, False
        
    # Eixo Y (Movimento Vertical)
    if dy == 1:  # 'a' está abaixo de 'b'. (No Pygame, o Y cresce para baixo).
        a.walls['top'], b.walls['bottom'] = False, False
    if dy == -1: # 'a' está acima de 'b'.
        a.walls['bottom'], b.walls['top'] = False, False

def heuristic(cell_a, cell_b):
    """
    Calcula a estimativa de custo de uma célula até o objetivo (o Queijo).
    Utiliza a 'Distância de Manhattan', que é a soma das diferenças absolutas
    das coordenadas X e Y. É a heurística ideal para grids onde o movimento 
    diagonal não é permitido.
    """
    return abs(cell_a.col - cell_b.col) + abs(cell_a.row - cell_b.row)

def generate_maze():
    """
    Gera o labirinto usando o algoritmo 'Recursive Backtracker' (Busca em Profundidade - DFS).
    Garante que todas as células sejam conectadas, criando um caminho único entre quaisquer dois pontos.
    """
    # Cria uma matriz 2D (lista de listas) preenchida com objetos da classe Cell
    grid = [[Cell(c, r) for r in range(ROWS)] for c in range(COLS)]
    
    # Define a célula inicial [0,0] e a marca como visitada
    current = grid[0][0]
    current.visited = True
    
    # A pilha (stack) guarda o histórico do caminho para podermos retroceder (backtrack)
    stack = [current]

    while stack:
        # Pega a célula atual (o topo da pilha)
        current = stack[-1]
        
        # Busca um vizinho aleatório que ainda não foi visitado (ignora paredes nesta fase)
        next_cell = current.check_neighbors(grid)
        
        if next_cell:
            # Se achou um vizinho livre, avança para ele
            next_cell.visited = True
            stack.append(next_cell) # Adiciona ao histórico
            remove_walls(current, next_cell) # Abre passagem entre eles
        else:
            # Beco sem saída: remove a célula atual da pilha para retroceder e tentar outro caminho
            stack.pop()
            
    return grid

def a_star(grid, start, end):
    """
    Algoritmo de Busca A* (A-Estrela).
    Encontra o caminho mais curto do 'start' até o 'end' avaliando o custo real (G) 
    e a heurística (H).
    """
    # open_set: Lista de células descobertas que precisam ser avaliadas
    open_set = [start]
    # closed_set: Lista de células que já foram avaliadas e não precisam ser revisitadas
    closed_set = []

    while open_set:
        # Encontra a célula no open_set que tem o menor custo total (F = G + H)
        current = min(open_set, key=lambda cell: cell.f)
        
        # Condição de Vitória: Chegamos no objetivo!
        if current == end:
            path = []
            # Reconstrói o caminho andando de trás para frente usando os ponteiros 'previous'
            while current:
                path.append(current)
                current = current.previous
            # Inverte a lista para retornar do início ao fim
            return path[::-1]

        # Move a célula atual da fila de 'a avaliar' para 'avaliadas'
        open_set.remove(current)
        closed_set.append(current)

        # Analisa os vizinhos acessíveis (respeitando as paredes geradas no labirinto)
        for neighbor in current.get_valid_neighbors(grid):
            # Se já avaliamos esse vizinho por completo, ignora
            if neighbor in closed_set: 
                continue
            
            # Custo G provisório: o custo para chegar até o atual + 1 passo
            temp_g = current.g + 1
            
            # Adiciona o vizinho na lista de avaliação se for novo
            if neighbor not in open_set:
                open_set.append(neighbor)
            # Se já estava na lista, mas este novo caminho até ele é pior (mais longo), ignora
            elif temp_g >= neighbor.g:
                continue

            # Se passou pelos filtros, este é o melhor caminho encontrado até agora para este vizinho!
            # Atualiza as variáveis matemáticas e registra de onde viemos
            neighbor.previous = current
            neighbor.g = temp_g
            neighbor.h = heuristic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h # F = G + H
            
    # Retorna uma lista vazia caso não encontre caminho (impossível no nosso gerador)
    return []