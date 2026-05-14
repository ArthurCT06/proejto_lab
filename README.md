# Documentação do Projeto: Labirinto A*

Este documento descreve a estrutura, o funcionamento e a comunicação entre os arquivos de código do projeto **Labirinto A***. O projeto é uma visualização gráfica de um algoritmo de busca de caminhos (A*) navegando por um labirinto gerado proceduralmente, implementado em Python utilizando a biblioteca Pygame.

## Visão Geral dos Arquivos

O projeto está modularizado em quatro arquivos principais, cada um com uma responsabilidade bem definida:

1.  `constants.py`: Configurações e parâmetros globais.
2.  `cell.py`: Definição da estrutura base do labirinto (a Célula).
3.  `algorithms.py`: Motores lógicos (geração do labirinto e algoritmo de busca A*).
4.  `main.py`: Ponto de entrada, interface gráfica e orquestração.

---

## 1. `constants.py` (Configurações)
Este arquivo atua como um repositório central para as configurações e constantes do projeto. Isso facilita ajustes rápidos de layout e design sem precisar alterar o código lógico.

**O que ele contém:**
*   **Dimensões da Janela:** `WIDTH` e `HEIGHT` (600x600 pixels).
*   **Dimensões da Matriz:** `COLS` e `ROWS` (20x20).
*   **Tamanho da Célula:** `CELL_SIZE` (calculado dinamicamente com base no tamanho da tela e da matriz).
*   **Paleta de Cores:** Definição de tuplas RGB para o fundo (`WHITE`), paredes (`BLACK`), rastro (`GREEN`), agente/rato (`BLUE`), objetivo/queijo (`YELLOW`), etc.

**Comunicação:** É importado por quase todos os outros arquivos (`cell.py`, `algorithms.py`, `main.py`) para garantir que todos usem as mesmas medidas e cores.

---

## 2. `cell.py` (Estrutura de Dados)
Define a classe `Cell`, que representa um único "quadradinho" no grid do labirinto.

**O que ele contém (Classe `Cell`):**
*   **Propriedades Físicas:** Coordenadas (`col`, `row`) e um dicionário `walls` que indica quais das 4 paredes estão de pé.
*   **Propriedades Visuais:** Método `draw()` que desenha as paredes usando as funções do Pygame.
*   **Propriedades Lógicas (Geração):** Atributo `visited` e método `check_neighbors()`, usados pelo algoritmo de geração de labirinto para saber por onde já passou (ignorando paredes).
*   **Propriedades Lógicas (Busca A*):** Variáveis de custo `g` (custo real), `h` (heurística), `f` (custo total) e `previous` (ponteiro para a célula anterior). Método `get_valid_neighbors()`, que retorna os vizinhos acessíveis (respeitando as paredes).

**Comunicação:** Utiliza as variáveis matemáticas de `constants.py`. Seus objetos são manipulados massivamente por `algorithms.py` (para criar caminhos) e por `main.py` (para desenhar tudo na tela).

---

## 3. `algorithms.py` (Lógica e Motores)
Isola toda a lógica complexa do sistema, separando-a da parte visual.

**O que ele contém:**
*   `remove_walls(a, b)`: Função auxiliar que descobre a posição relativa de duas células vizinhas e "derruba" (altera para `False`) a parede compartilhada entre elas.
*   `generate_maze()`: Utiliza o algoritmo *Recursive Backtracker* (Busca em Profundidade) para criar o labirinto. Ele instancia uma matriz de objetos `Cell`, anda aleatoriamente marcando as células como `visited` e chamando `remove_walls()` para abrir passagens, retornando o `grid` final.
*   `heuristic(cell_a, cell_b)`: Calcula a Distância de Manhattan (diferença absoluta em X e Y) entre duas células, servindo como estimativa para o A*.
*   `a_star(grid, start, end)`: O cérebro da busca. Analisa a matriz de células, calcula os custos (`g`, `h`, `f`) de cada `Cell`, e explora os caminhos possíveis usando o método `get_valid_neighbors()`. Ao encontrar o destino, retrocede usando o atributo `previous` para devolver a lista do caminho final.

**Comunicação:** Instancia os objetos `Cell` (de `cell.py`) e os devolve prontos para o `main.py`. Utiliza as constantes dimensionais de `constants.py`.

---

## 4. `main.py` (Interface e Orquestrador)
É o ponto de partida da aplicação. Inicializa a janela gráfica, lida com os eventos de usuário (teclado/mouse) e renderiza a animação.

**O que ele contém:**
*   **Loop Externo (Gestor de Ambiente):** Roda para inicializar uma "nova fase". Chama o `generate_maze()` para criar o cenário e roda o `a_star()` de forma invisível para precalcular o caminho completo.
*   **Loop Interno (Renderizador de Frames):** Roda continuamente para desenhar a interface. Ele pinta o fundo de branco, pede para cada `Cell` desenhar suas paredes, desenha o Queijo e o caminho Verde percorrido até o momento, e avança a posição do Rato (`path_index`) quadro a quadro.
*   **Término e Overlay:** Quando a animação termina, calcula o tempo e os passos dados, renderizando uma tela translúcida (overlay) com as estatísticas finais.

**Comunicação:** Importa as funções geradoras de `algorithms.py`, as constantes de `constants.py`, e utiliza os métodos e propriedades visuais dos objetos instanciados da classe `Cell`.

---

## Fluxo de Execução Resumido

1. Ao rodar `main.py`, a tela gráfica é inicializada.
2. O `main.py` solicita a `algorithms.py` a geração de um novo labirinto.
3. `algorithms.py` cria uma grade 20x20 instanciando 400 objetos da classe `Cell` (de `cell.py`) e escava o labirinto modificando os atributos `walls` dessas células.
4. O `main.py` então solicita a `algorithms.py` que resolva o labirinto recém-criado, passando a célula inicial e a final.
5. O algoritmo `a_star` calcula o caminho, manipulando as variáveis `f`, `g`, `h` e `previous` de cada `Cell`, e devolve uma lista com o caminho vencedor.
6. Finalmente, o `main.py` entra em seu loop visual (FPS), desenhando a matriz na tela usando o método `draw()` de cada `Cell` e animando o movimento do agente pelo caminho pré-calculado.
