"""
Interfaz gráfica del juego (menú, tablero, pantallas)
"""
import pygame
from constants import *

class GameUI:
    """Maneja todo el renderizado gráfico del juego"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        
        # Cargar imágenes
        self.load_images()
    
    def load_images(self):
        """Carga las imágenes de los caballos"""
        try:
            white_knight_img = pygame.image.load("players/white_horse.png")
            black_knight_img = pygame.image.load("players/black_horse.png")
            
            self.white_knight = pygame.transform.scale(white_knight_img, (CELL_SIZE, CELL_SIZE))
            self.black_knight = pygame.transform.scale(black_knight_img, (CELL_SIZE, CELL_SIZE))
        except pygame.error as e:
            print(f"Error cargando imágenes: {e}")
            import sys
            sys.exit(1)
    
    def draw_menu(self):
        """Dibuja el menú principal"""
        self.screen.fill(WHITE)
        
        # Título
        title = self.title_font.render("SMART HORSES", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtítulo
        subtitle = self.font.render("Selecciona el nivel de dificultad", True, TEXT_COLOR)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 180))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Botones
        buttons = [
            ("Principiante (Profundidad 2)", "principiante", 250),
            ("Amateur (Profundidad 4)", "amateur", 350),
            ("Experto (Profundidad 6)", "experto", 450)
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        menu_buttons = []
        
        for text, difficulty, y in buttons:
            button_rect = pygame.Rect(WINDOW_WIDTH//2 - 200, y, 400, 60)
            
            color = BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            
            pygame.draw.rect(self.screen, color, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, button_rect, 3, border_radius=10)
            
            button_text = self.font.render(text, True, WHITE)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
            
            menu_buttons.append((button_rect, difficulty))
        
        return menu_buttons
    
    def draw_board(self, board, machine_pos, player_pos, destroyed, 
                   selected_pos, valid_moves):
        """Dibuja el tablero de juego"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = BOARD_OFFSET_X + col * CELL_SIZE
                y = BOARD_OFFSET_Y + row * CELL_SIZE
                
                # Color de casilla
                if (row, col) in destroyed:
                    color = DESTROYED_COLOR
                elif (row + col) % 2 == 0:
                    color = LIGHT_SQUARE
                else:
                    color = DARK_SQUARE
                
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                
                # Resaltar selección
                if selected_pos == (row, col):
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    s.fill(HIGHLIGHT_COLOR)
                    self.screen.blit(s, (x, y))
                
                # Resaltar movimientos válidos
                if (row, col) in valid_moves:
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    s.fill(MOVE_HIGHLIGHT)
                    self.screen.blit(s, (x, y))
                
                # Dibujar valores de puntos
                if (row, col) not in destroyed:
                    cell_value = board[row][col]
                    if isinstance(cell_value, int):
                        color = POSITIVE_POINTS if cell_value > 0 else NEGATIVE_POINTS
                        text = self.font.render(f"{cell_value:+d}", True, color)
                        text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                        self.screen.blit(text, text_rect)
        
        # Dibujar caballos
        if machine_pos and machine_pos not in destroyed:
            x = BOARD_OFFSET_X + machine_pos[1] * CELL_SIZE
            y = BOARD_OFFSET_Y + machine_pos[0] * CELL_SIZE
            self.screen.blit(self.white_knight, (x, y))
        
        if player_pos and player_pos not in destroyed:
            x = BOARD_OFFSET_X + player_pos[1] * CELL_SIZE
            y = BOARD_OFFSET_Y + player_pos[0] * CELL_SIZE
            self.screen.blit(self.black_knight, (x, y))
        
        # Borde del tablero
        pygame.draw.rect(self.screen, BLACK, 
                        (BOARD_OFFSET_X, BOARD_OFFSET_Y, 
                         CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE), 3)
    
    def draw_info_panel(self, difficulty, max_depth, machine_score, player_score,
                       current_turn, game_over, machine_skipped, player_skipped):
        """Dibuja el panel de información lateral"""
        panel_x = BOARD_OFFSET_X + CELL_SIZE * BOARD_SIZE + 30
        panel_y = BOARD_OFFSET_Y
        
        # Título
        title = self.title_font.render("SMART HORSES", True, TEXT_COLOR)
        self.screen.blit(title, (panel_x, panel_y))
        
        # Dificultad
        diff_text = self.small_font.render(f"Nivel: {difficulty.capitalize()}", True, TEXT_COLOR)
        self.screen.blit(diff_text, (panel_x, panel_y + 60))
        
        depth_text = self.small_font.render(f"Profundidad: {max_depth}", True, TEXT_COLOR)
        self.screen.blit(depth_text, (panel_x, panel_y + 85))
        
        # Puntuaciones
        y_offset = 140
        
        machine_label = self.font.render("Máquina (Blanco):", True, TEXT_COLOR)
        self.screen.blit(machine_label, (panel_x, panel_y + y_offset))
        
        machine_score_text = self.font.render(f"{machine_score} puntos", True, POSITIVE_POINTS)
        self.screen.blit(machine_score_text, (panel_x, panel_y + y_offset + 30))
        
        y_offset += 100
        player_label = self.font.render("Jugador (Negro):", True, TEXT_COLOR)
        self.screen.blit(player_label, (panel_x, panel_y + y_offset))
        
        player_score_text = self.font.render(f"{player_score} puntos", True, NEGATIVE_POINTS)
        self.screen.blit(player_score_text, (panel_x, panel_y + y_offset + 30))
        
        # Turno actual
        y_offset += 100
        if not game_over:
            turn_text = "Turno: " + ("Máquina" if current_turn == "MACHINE" else "Jugador")
            turn_label = self.font.render(turn_text, True, TEXT_COLOR)
            self.screen.blit(turn_label, (panel_x, panel_y + y_offset))
            
            if machine_skipped:
                skip_text = self.small_font.render("(Máquina sin movimientos: -4)", 
                                                   True, NEGATIVE_POINTS)
                self.screen.blit(skip_text, (panel_x, panel_y + y_offset + 30))
            elif player_skipped:
                skip_text = self.small_font.render("(Jugador sin movimientos: -4)", 
                                                   True, NEGATIVE_POINTS)
                self.screen.blit(skip_text, (panel_x, panel_y + y_offset + 30))
        
        # Instrucciones
        y_offset += 80
        inst1 = self.small_font.render("Haz clic en tu caballo", True, TEXT_COLOR)
        inst2 = self.small_font.render("y luego en el destino", True, TEXT_COLOR)
        inst3 = self.small_font.render("Clic derecho: deseleccionar", True, TEXT_COLOR)
        self.screen.blit(inst1, (panel_x, panel_y + y_offset))
        self.screen.blit(inst2, (panel_x, panel_y + y_offset + 25))
        self.screen.blit(inst3, (panel_x, panel_y + y_offset + 50))
    
    def draw_game_over(self, winner, machine_score, player_score):
        """Dibuja la pantalla de fin de juego"""
        # Overlay semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Panel central
        panel_rect = pygame.Rect(WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2 - 200, 500, 400)
        pygame.draw.rect(self.screen, WHITE, panel_rect, border_radius=20)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 5, border_radius=20)
        
        # Título
        if winner == "PLAYER":
            title_text = "¡GANASTE!"
            color = POSITIVE_POINTS
        elif winner == "MACHINE":
            title_text = "LA MÁQUINA GANÓ"
            color = NEGATIVE_POINTS
        else:
            title_text = "¡EMPATE!"
            color = TEXT_COLOR
        
        title = self.title_font.render(title_text, True, color)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 120))
        self.screen.blit(title, title_rect)
        
        # Puntuaciones finales
        machine_text = self.font.render(f"Máquina: {machine_score} puntos", True, TEXT_COLOR)
        machine_rect = machine_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 40))
        self.screen.blit(machine_text, machine_rect)
        
        player_text = self.font.render(f"Jugador: {player_score} puntos", True, TEXT_COLOR)
        player_rect = player_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 10))
        self.screen.blit(player_text, player_rect)
        
        # Botones
        mouse_pos = pygame.mouse.get_pos()
        
        play_rect = pygame.Rect(WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2 + 80, 360, 50)
        play_color = BUTTON_HOVER if play_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, play_color, play_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, play_rect, 3, border_radius=10)
        
        play_text = self.font.render("Jugar de Nuevo", True, WHITE)
        play_text_rect = play_text.get_rect(center=play_rect.center)
        self.screen.blit(play_text, play_text_rect)
        
        menu_rect = pygame.Rect(WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2 + 150, 360, 50)
        menu_color = BUTTON_HOVER if menu_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, menu_color, menu_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, menu_rect, 3, border_radius=10)
        
        menu_text = self.font.render("Menú Principal", True, WHITE)
        menu_text_rect = menu_text.get_rect(center=menu_rect.center)
        self.screen.blit(menu_text, menu_text_rect)
        
        return [(play_rect, "PLAY_AGAIN"), (menu_rect, "MENU")]