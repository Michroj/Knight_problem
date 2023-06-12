import pygame
import sys



knight_x=0
knight_y=0
# Ustalenie kolorów
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 153, 0)


def menu():
    BOARD_SIZE = int(input("Enter the size of the chessboard: "))
    knight_x = int(input("Enter the x-coordinate of the knight's position (0 to {}): ".format(BOARD_SIZE-1)))
    knight_y = int(input("Enter the y-coordinate of the knight's position (0 to {}): ".format(BOARD_SIZE-1)))
    WINDOW_SIZE = 600
    CELL_SIZE = WINDOW_SIZE // BOARD_SIZE
    start(WINDOW_SIZE,BOARD_SIZE,knight_x,knight_y,CELL_SIZE)
    menu()



def is_valid_move(x, y, n, visited):
    """
    Sprawdza, czy ruch jest możliwy na planszy n x n
    i czy pole nie zostało odwiedzone wcześniej.
    """
    if x >= 0 and y >= 0 and x < n and y < n and visited[x][y] == 0:
        return True
    return False

def dfs(x, y, n, visited, path, move_count):
    """
    Funkcja przeszukiwania w głąb (DFS) do generowania ścieżki skoczka.
    """
    # Jeśli odwiedzono wszystkie pola, zwraca ścieżkę
    if move_count == n * n:
        return True, path
    
    # Lista możliwych ruchów skoczka
    moves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]

    # Próba wykonania ruchu w każdym z możliwych kierunków
    for move in moves:
        new_x = x + move[0]
        new_y = y + move[1]
        if is_valid_move(new_x, new_y, n, visited):
            visited[new_x][new_y] = move_count + 1
            path.append((new_x, new_y))
            found, result_path = dfs(new_x, new_y, n, visited, path, move_count + 1)
            if found:
                return True, result_path
            # Jeśli nie znaleziono ścieżki, cofa się do poprzedniego pola
            path.pop()
            visited[new_x][new_y] = 0
    return False, None

# Funkcja do rysowania planszy
def draw_board(screen,BOARD_SIZE,CELL_SIZE):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            color = WHITE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(screen, color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))



def draw_knight(x, y,screen,CELL_SIZE,knight_image):
  # Załaduj obrazek rycerza
      # Zmień rozmiar obrazka
    screen.blit(knight_image, (x * CELL_SIZE, y * CELL_SIZE))

# Początkowe położenie skoczka


def draw_path(screen, path,CELL_SIZE,BOARD_SIZE,knight_image):

     for i, (x, y) in enumerate(path):
        # Rysowanie planszy
        draw_board(screen,BOARD_SIZE,CELL_SIZE)

        # Rysowanie czarnych kropek na poprzednich polach
        for j, (row, col) in enumerate(path[:i]):
            pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 5)

        draw_knight(y, x,screen,CELL_SIZE,knight_image) # Rysowanie obrazka skoczka na aktualnym polu
        pygame.display.flip() # Aktualizacja ekranu
        pygame.time.delay(500)  # Dodaj odstęp czasowy 500 ms


def generate_knight_tour(n, start_x, start_y):
    """
    Główna funkcja generująca ścieżkę skoczka na szachownicy.
    """
    # Inicjalizacja planszy i list
    visited = [[0 for _ in range(n)] for _ in range(n)]
    visited[start_x][start_y] = 1
    path = [(start_x, start_y)]

    # Generowanie ścieżki skoczka za pomocą przeszukiwania w głąb (DFS)
    found, result_path = dfs(start_x, start_y, n, visited, path, 1)

    if found:
        return result_path
    else:
        return None


def start(WINDOW_SIZE,BOARD_SIZE,knight_x,knight_y,CELL_SIZE):
    # Inicjalizacja Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Ścieżka skoczka na szachownicy")
    knight_image = pygame.image.load("knight.png")
    knight_image = pygame.transform.scale(knight_image, (CELL_SIZE, CELL_SIZE))
    # Pobranie ścieżki skoczka dla planszy nxn, startującego z pola (0, 0)
    knight_path = generate_knight_tour(BOARD_SIZE, knight_x,knight_y )

    if knight_path is not None:
    # Jeśli ścieżka została znaleziona, rysuje planszę i ścieżkę na ekranie
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            draw_board(screen,BOARD_SIZE,CELL_SIZE)
            draw_path(screen, knight_path,CELL_SIZE,BOARD_SIZE,knight_image)
            pygame.display.flip()
    else:
    # Jeśli nie udało się wygenerować ścieżki, wypisuje komunikat
        print("Nie udało się wygenerować ścieżki skoczka na szachownicy.")
        pygame.quit()

menu()

