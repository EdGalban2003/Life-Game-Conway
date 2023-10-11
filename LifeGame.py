import pygame
import numpy as np

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 1500, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego de la Vida")

# Variables para el juego
cell_size = 20
menu_width = 200  # Ancho de la barra de menú
game_width = width - menu_width  # Ancho del área de juego
game_height = height  # Altura del área de juego
grid_rows, grid_cols = game_height // cell_size, game_width // cell_size
grid = np.zeros((grid_rows, grid_cols), dtype=int)  # Inicialmente, todas las celdas están muertas
running = True
drawing = False  # Indica si el usuario está dibujando en la cuadrícula

# Variables para el control del tiempo
auto_advance = False
auto_advance_interval = 150  # Intervalo de 1 segundo en milisegundos
last_advance_time = pygame.time.get_ticks()

# Variables para el contador de generación
generation = 0

# Variable para controlar el avance generación por generación
step_by_step = False

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)  # Gris para el contador de generación

# Fuente para el contador de generación
font = pygame.font.Font(None, 36)

# Define varios patrones predefinidos como listas de coordenadas (row, col)
patterns = [
    [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],  # Nave espacial
    [(0, 0), (0, 1), (0, 2)],  # Línea
    [(0, 1), (0, 3), (1, 0), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (4, 2)], # Pulsar
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0)],  # Nave de Células Cruzadas
    [(0, 0), (0, 1), (0, 4), (0, 5),
     (1, 1), (1, 5),
     (2, 0), (2, 2), (2, 3), (2, 5),
     (3, 0), (3, 3), (3, 5),
     (4, 0), (4, 5),
     (5, 0), (5, 1), (5, 4), (5, 5)],  # Compuerta Lógica OR
    [(0, 2), (0, 3), (0, 4), (0, 5),
     (1, 1), (1, 2), (1, 4), (1, 5),
     (2, 1), (2, 5),
     (3, 0), (3, 3), (3, 5),
     (4, 1), (4, 4),
     (5, 2), (5, 3)],  # Compuerta Lógica AND
    [(0, 1), (0, 4),
     (1, 2), (1, 3),
     (2, 0), (2, 5),
     (3, 2), (3, 3),
     (4, 1), (4, 4),
     (5, 1), (5, 4)],  # Compuerta Lógica XOR
]

# Nombres de los patrones
pattern_names = [
    "Nave espacial",
    "Línea",
    "Pulsar",
    "Nave de Células Cruzadas",
    "Compuerta Lógica OR",
    "Compuerta Lógica AND",
    "Compuerta Lógica XOR",
]

# Función para configurar la cuadrícula con un patrón seleccionado
def set_pattern(pattern):
    for row, col in pattern:
        grid_row = grid_rows // 2 - len(pattern) // 2 + row
        grid_col = grid_cols // 2 - len(pattern[0]) // 2 + col
        if 0 <= grid_row < grid_rows and 0 <= grid_col < grid_cols:
            grid[grid_row][grid_col] = 1

# Índice del patrón seleccionado actualmente
selected_pattern_index = 0

# Función para configurar la cuadrícula con un patrón seleccionado
def set_pattern(pattern):
    for row, col in pattern:
        grid_row = grid_rows // 2 + row
        grid_col = grid_cols // 2 + col
        if 0 <= grid_row < grid_rows and 0 <= grid_col < grid_cols:
            grid[grid_row][grid_col] = 1

# Función para dibujar botones en la barra de menú
def draw_menu():
    menu_height = game_height
    button_height = 50
    button_width = 150
    button_spacing = 10
    x = game_width + 10  # Posición horizontal para los botones
    y = 10
    
    for i, pattern in enumerate(patterns):
        pygame.draw.rect(screen, WHITE, (x, y, button_width, button_height))
        text = font.render(pattern_names[i], True, BLACK)  # Mostrar el nombre del patrón
        screen.blit(text, (x + 10, y + 10))
        y += button_height + button_spacing
        
        # Detecta clic en el botón
        if x <= pygame.mouse.get_pos()[0] <= x + button_width and y - button_height <= pygame.mouse.get_pos()[1] <= y:
            if pygame.mouse.get_pressed()[0]:
                set_pattern(pattern)

# Función para dibujar el contador de generación
def draw_generation_counter():
    text = font.render("Generación: " + str(generation), True, GRAY)
    screen.blit(text, (game_width + 10, game_height - 40))  # Posición del contador

# Función para dibujar la cuadrícula
def draw_grid():
    for row in range(grid_rows):
        for col in range(grid_cols):
            x = col * cell_size
            y = row * cell_size
            # Define el color de las celdas
            cell_color = WHITE if grid[row][col] == 1 else BLACK
            pygame.draw.rect(screen, cell_color, (x, y, cell_size, cell_size))
            
            # Define el color de las líneas de la cuadrícula
            line_color = (9, 9, 9)  # Gris oscuro (puedes ajustar los valores RGB según tu preferencia)
            pygame.draw.rect(screen, line_color, (x, y, cell_size, cell_size), 1)

# Función para calcular la siguiente generación del Juego de la Vida
def next_generation():
    new_grid = np.zeros((grid_rows, grid_cols), dtype=int)
    for row in range(grid_rows):
        for col in range(grid_cols):
            neighbors = np.sum(grid[row - 1:row + 2, col - 1:col + 2]) - grid[row][col]
            if grid[row][col] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0
                else:
                    new_grid[row][col] = 1
            else:
                if neighbors == 3:
                    new_grid[row][col] = 1
    return new_grid

# Ciclo principal del juego
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Click izquierdo para dibujar o borrar
                if 0 <= pygame.mouse.get_pos()[0] <= game_width and 0 <= pygame.mouse.get_pos()[1] <= game_height:
                    x, y = pygame.mouse.get_pos()
                    col = x // cell_size
                    row = y // cell_size
                    grid[row][col] = 1 - grid[row][col]  # Alternar entre vivo y muerto
                    drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                grid = next_generation()  # Avanzar 1 generación con la barra espaciadora
                generation += 1  # Incrementar el contador de generación
            elif event.key == pygame.K_c:
                if not step_by_step:
                    grid = np.zeros((grid_rows, grid_cols), dtype=int)  # Limpiar la cuadrícula con la tecla 'C'
                    generation = 0  # Reiniciar el contador de generación
                step_by_step = not step_by_step  # Alternar el modo de avance generación por generación
            elif event.key == pygame.K_v:
                auto_advance = not auto_advance  # Alternar avance automático con la tecla 'V'

    if auto_advance and current_time - last_advance_time >= auto_advance_interval:
        grid = next_generation()
        last_advance_time = current_time
        generation += 1  # Incrementar el contador de generación
    elif step_by_step:  # Avance generación por generación
        step_by_step = False  # Detener el avance después de una generación

    screen.fill(BLACK)
    draw_grid()
    draw_menu()  # Dibujar la barra de menú
    draw_generation_counter()  # Dibujar el contador de generación
    
    pygame.display.flip()

# Salir del juego
pygame.quit()