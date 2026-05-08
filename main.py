import pygame
import random
from constants import *
from algorithms import generate_maze, a_star

def draw_text_center(surface, text, font, color, y_offset=0):
    """
    Função auxiliar para centralizar e desenhar textos na tela.
    O Pygame não escreve texto diretamente na tela; ele primeiro "renderiza" 
    o texto em uma imagem (Surface) e depois "carimba" (blit) essa imagem na tela principal.
    """
    # 1. Cria a imagem contendo o texto
    text_surface = font.render(text, True, color)
    # 2. Pega o retângulo imaginário que envolve esse texto e define o centro dele 
    # para ser o centro da tela (ajustado pelo y_offset para pular linhas)
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2 + y_offset))
    # 3. Carimba o texto na superfície (tela) nas coordenadas calculadas
    surface.blit(text_surface, text_rect)

def main():
    """
    Função principal que orquestra a interface gráfica e os motores lógicos do jogo.
    Utiliza uma arquitetura de 'Dois Loops' para permitir o reinício contínuo do labirinto.
    """
    # --- INICIALIZAÇÃO DO MOTOR GRÁFICO ---
    pygame.init()
    pygame.font.init() # Prepara o Pygame para renderizar fontes de texto
    
    # Cria a janela principal do programa com as dimensões constantes
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Labirinto A* - Modularizado")
    
    # O relógio controla a taxa de atualização (FPS) da tela
    clock = pygame.time.Clock()
    
    # Carrega as fontes do sistema para usar no menu final
    font = pygame.font.SysFont('Arial', 24)
    large_font = pygame.font.SysFont('Arial', 32, bold=True)

    # ==========================================
    # CONTROLE DE VELOCIDADE DA ANIMAÇÃO
    # ==========================================
    # 50  = Muito rápido
    # 100 = Normal
    # 250 = Lento (Ideal para explicar o passo a passo)
    # 500 = Muito lento (Meio segundo por casa)
    ANIMATION_SPEED = 100
    # ==========================================

    # Variável de controle do Ciclo de Vida da Aplicação
    app_running = True
    
    # ==========================================
    # 1. LOOP EXTERNO: O GESTOR DE AMBIENTE
    # ==========================================
    # Sempre que este loop recomeça, um cenário 100% novo é criado do zero.
    while app_running:
        
        # --- PREPARAÇÃO DOS DADOS (Back-end) ---
        grid = generate_maze()
        
        # Define o rato na posição [0][0]
        start_cell = grid[0][0]
        # Escolhe uma posição aleatória para o queijo, evitando as bordas [0] para não sobrepor o rato
        end_cell = grid[random.randint(1, COLS-1)][random.randint(1, ROWS-1)]
        
        # Roda a Inteligência Artificial ANTES da tela começar a atualizar.
        # A animação é apenas o programa lendo essa lista precalculada.
        path = a_star(grid, start_cell, end_cell)
        path_index = 0 # Usado para controlar em qual passo da animação o rato está
        
        # pygame.time.get_ticks() retorna os milissegundos desde que o pygame.init() foi chamado
        start_time = pygame.time.get_ticks() 
        end_time = 0
        finished = False # Flag de controle de término do percurso

        # Variável de controle da Partida Atual
        game_running = True
        
        # ==========================================
        # 2. LOOP INTERNO: O RENDERIZADOR DE FRAMES
        # ==========================================
        # Este loop roda repetidamente (ex: 60 vezes por segundo) para desenhar a animação.
        while game_running:
            # Limpa a tela pintando-a de branco a cada frame (evita o efeito "borrão")
            screen.fill(WHITE)
            
            # --- ESCUTADOR DE EVENTOS ---
            for event in pygame.event.get():
                # Se o usuário clicar no 'X' da janela do Windows/Mac
                if event.type == pygame.QUIT:
                    game_running = False # Quebra o loop atual
                    app_running = False  # Quebra o loop mestre (fecha o programa)
                
                # Só começa a escutar o teclado SE o rato já chegou no queijo (finished == True)
                if finished and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: 
                        # Aperto [R]: Encerra a partida atual, mas mantém o app_running = True.
                        # Isso faz o programa voltar para o topo do Loop Externo e gerar novo grid.
                        game_running = False    
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        # Aperto [Q] ou [ESC]: Encerra tudo
                        game_running = False
                        app_running = False

            # --- DESENHO DO CENÁRIO ---
            # 1. Pede para cada célula da matriz desenhar suas paredes de pé
            for col in range(COLS):
                for row in range(ROWS): 
                    grid[col][row].draw(screen)

            # 2. Desenha o Queijo (Um retângulo amarelo ligeiramente menor que a célula)
            pygame.draw.rect(screen, YELLOW, (end_cell.col * CELL_SIZE + 5, end_cell.row * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))

            # 3. Desenha o rastro (Caminho Verde) percorrido até o passo atual da animação
            for i in range(path_index):
                p = path[i]
                pygame.draw.rect(screen, GREEN, (p.col * CELL_SIZE + 8, p.row * CELL_SIZE + 8, CELL_SIZE - 16, CELL_SIZE - 16))

            # --- MOTOR DE ANIMAÇÃO ---
            # Se o caminho existe e ainda não terminamos de andar por ele
            if path and path_index < len(path):
                # Desenha o Rato na célula correspondente ao índice atual
                curr = path[path_index]
                pygame.draw.circle(screen, BLUE, (curr.col * CELL_SIZE + CELL_SIZE//2, curr.row * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)
                
                # Pausa o programa pela quantidade de milissegundos definida na variável
                pygame.time.delay(ANIMATION_SPEED)
                
                # Avança para o próximo passo no frame seguinte
                path_index += 1
            else:
                # O rato terminou de andar e chegou no final.
                # Mantém o rato desenhado em cima do queijo.
                pygame.draw.circle(screen, BLUE, (end_cell.col * CELL_SIZE + CELL_SIZE//2, end_cell.row * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)
                
                # Gatilho de Término (Só entra aqui no exato milissegundo em que chega)
                if not finished:
                    finished = True
                    end_time = pygame.time.get_ticks() # Registra o tempo final
                
                # --- TELA DE RESULTADOS (OVERLAY) ---
                # Cria uma "película" do tamanho da tela inteira
                overlay = pygame.Surface((WIDTH, HEIGHT))
                # Aplica o canal Alpha (Transparência). 0 = Invisível, 255 = Opaco total.
                overlay.set_alpha(200) 
                overlay.fill(BLACK) # Pinta a película de preto translúcido
                screen.blit(overlay, (0, 0)) # Carimba a película na coordenada [0,0] (canto superior esquerdo)
                
                # --- CÁLCULO DE ESTATÍSTICAS ---
                # Pega a diferença do tempo final e inicial. Divide por 1000 para converter ms para segundos.
                time_taken = (end_time - start_time) / 1000 
                # Subtrai 1 do len(path) porque o ponto de partida [0,0] não conta como um passo/custo.
                steps = len(path) - 1 
                
                # Escreve o painel final sobre a tela escurecida
                draw_text_center(screen, "BUSCA CONCLUÍDA!", large_font, WHITE, -60)
                draw_text_center(screen, f"Tempo de percurso: {time_taken:.1f} segundos", font, WHITE, -10)
                draw_text_center(screen, f"Custo do Caminho (Passos): {steps}", font, WHITE, 20)
                draw_text_center(screen, "[R] Reiniciar novo labirinto   |   [Q] Fechar", font, YELLOW, 80)

            # --- ATUALIZAÇÃO DO DISPLAY ---
            # Troca o buffer de vídeo e mostra o desenho que acabamos de montar na tela
            pygame.display.flip()
            # Força o loop a rodar no máximo 60 vezes por segundo
            clock.tick(60)

    # Desliga os módulos do Pygame e devolve a memória ao sistema operativo quando o while encerra
    pygame.quit()

if __name__ == "__main__":
    main()