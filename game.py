"""
Lógica principal del juego Smart Horses
"""
import pygame
import random
from typing import Tuple
from constants import *
from minimax import MinimaxAI
from ui import GameUI

class SmartHorsesGame:
    """Clase principal que gestiona el juego"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Smart Horses")
        self.clock = pygame.time.Clock()
        
        # Componentes
        self.ui = GameUI(self.screen)
        self.ai = MinimaxAI(BOARD_SIZE)
        
        # Estados
        self.state = "MENU"
        self.difficulty = None
        self.max_depth = 0
        
        # Tablero
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.machine_pos = None
        self.player_pos = None
        self.destroyed = set()
        
        # Puntuaciones
        self.machine_score = 0
        self.player_score = 0
        
        # Control
        self.current_turn = "MACHINE"
        self.selected_pos = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.machine_skipped = False
        self.player_skipped = False
        
        self.menu_buttons = []
        self.gameover_buttons = []
    
    def initialize_game(self, difficulty: str):
        """Inicializa una nueva partida"""
        self.difficulty = difficulty
        self.max_depth = DIFFICULTY_DEPTH[difficulty]
        
        # Reiniciar
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.destroyed = set()
        self.machine_score = 0
        self.player_score = 0
        self.current_turn = "MACHINE"
        self.selected_pos = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.machine_skipped = False
        self.player_skipped = False
        
        # Posiciones aleatorias
        all_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]
        random.shuffle(all_positions)
        
        self.machine_pos = all_positions[0]
        self.player_pos = all_positions[1]
        
        # Colocar caballos
        self.board[self.machine_pos[0]][self.machine_pos[1]] = 'M'
        self.board[self.player_pos[0]][self.player_pos[1]] = 'P'
        
        # Colocar puntos
        for i, value in enumerate(POINT_VALUES):
            pos = all_positions[i + 2]
            self.board[pos[0]][pos[1]] = value
        
        self.state = "PLAYING"
        
        # Turno de la máquina
        if self.current_turn == "MACHINE":
            pygame.time.set_timer(pygame.USEREVENT, 1000, 1)
    
    def get_knight_moves(self, pos: Tuple[int, int]) -> list:
        """Obtiene movimientos válidos del caballo"""
        return self.ai.get_valid_moves(pos, self.destroyed)
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                  is_machine: bool) -> int:
        """Realiza un movimiento"""
        points = 0
        cell_value = self.board[to_pos[0]][to_pos[1]]
        if isinstance(cell_value, int):
            points = cell_value
        
        # Actualizar tablero
        self.board[from_pos[0]][from_pos[1]] = None
        self.board[to_pos[0]][to_pos[1]] = 'M' if is_machine else 'P'
        
        # Destruir casilla origen
        self.destroyed.add(from_pos)
        
        # Actualizar posición y puntuación
        if is_machine:
            self.machine_pos = to_pos
            self.machine_score += points
        else:
            self.player_pos = to_pos
            self.player_score += points
        
        return points
    
    def machine_turn(self):
        """Ejecuta el turno de la máquina"""
        moves = self.get_knight_moves(self.machine_pos)
        
        if not moves:
            player_moves = self.get_knight_moves(self.player_pos)
            if player_moves:
                self.machine_score -= PENALTY_POINTS
                self.machine_skipped = True
            self.current_turn = "PLAYER"
            self.check_game_over()
            return
        
        self.machine_skipped = False
        best_move = self.ai.get_best_move(
            self.machine_pos, self.player_pos, self.destroyed,
            self.machine_score, self.player_score, self.board, self.max_depth
        )
        
        if best_move:
            self.make_move(self.machine_pos, best_move, True)
        
        self.current_turn = "PLAYER"
        self.check_game_over()
    
    def check_game_over(self):
        """Verifica si el juego terminó"""
        machine_moves = self.get_knight_moves(self.machine_pos)
        player_moves = self.get_knight_moves(self.player_pos)
        
        if not machine_moves and not player_moves:
            self.game_over = True
            if self.machine_score > self.player_score:
                self.winner = "MACHINE"
            elif self.player_score > self.machine_score:
                self.winner = "PLAYER"
            else:
                self.winner = "TIE"
            self.state = "GAME_OVER"
    
    def handle_click(self, pos: Tuple[int, int], button: int):
        """Maneja los clics del mouse"""
        if self.state == "MENU":
            if button == 1:
                for rect, difficulty in self.menu_buttons:
                    if rect.collidepoint(pos):
                        self.initialize_game(difficulty)
                        break
        
        elif self.state == "GAME_OVER":
            if button == 1:
                for rect, action in self.gameover_buttons:
                    if rect.collidepoint(pos):
                        if action == "PLAY_AGAIN":
                            self.initialize_game(self.difficulty)
                        elif action == "MENU":
                            self.state = "MENU"
                        break
        
        elif self.state == "PLAYING" and self.current_turn == "PLAYER":
            player_moves = self.get_knight_moves(self.player_pos)
            
            if not player_moves:
                machine_moves = self.get_knight_moves(self.machine_pos)
                if machine_moves:
                    self.player_score -= PENALTY_POINTS
                    self.player_skipped = True
                else:
                    self.player_skipped = False
                
                self.current_turn = "MACHINE"
                self.check_game_over()
                
                if not self.game_over:
                    pygame.time.set_timer(pygame.USEREVENT, 1000, 1)
                return
            
            self.player_skipped = False
            
            # Clic derecho: deseleccionar
            if button == 3:
                self.selected_pos = None
                self.valid_moves = []
                return
            
            # Clic izquierdo: seleccionar o mover
            if button == 1:
                board_x = (pos[0] - BOARD_OFFSET_X) // CELL_SIZE
                board_y = (pos[1] - BOARD_OFFSET_Y) // CELL_SIZE
                
                if 0 <= board_x < BOARD_SIZE and 0 <= board_y < BOARD_SIZE:
                    clicked_pos = (board_y, board_x)
                    
                    if clicked_pos == self.player_pos:
                        self.selected_pos = clicked_pos
                        self.valid_moves = self.get_knight_moves(self.player_pos)
                    
                    elif clicked_pos in self.valid_moves:
                        self.make_move(self.player_pos, clicked_pos, False)
                        self.selected_pos = None
                        self.valid_moves = []
                        self.current_turn = "MACHINE"
                        self.check_game_over()
                        
                        if not self.game_over:
                            pygame.time.set_timer(pygame.USEREVENT, 1000, 1)
                    
                    else:
                        self.selected_pos = None
                        self.valid_moves = []
    
    def run(self):
        """Bucle principal del juego"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)
                
                elif event.type == pygame.USEREVENT:
                    if self.state == "PLAYING" and self.current_turn == "MACHINE":
                        self.machine_turn()
            
            # Renderizar
            self.screen.fill(WHITE)
            
            if self.state == "MENU":
                self.menu_buttons = self.ui.draw_menu()
            
            elif self.state == "PLAYING":
                self.ui.draw_board(self.board, self.machine_pos, self.player_pos,
                                  self.destroyed, self.selected_pos, self.valid_moves)
                self.ui.draw_info_panel(self.difficulty, self.max_depth,
                                       self.machine_score, self.player_score,
                                       self.current_turn, self.game_over,
                                       self.machine_skipped, self.player_skipped)
                
                if self.game_over:
                    self.gameover_buttons = self.ui.draw_game_over(
                        self.winner, self.machine_score, self.player_score
                    )
            
            elif self.state == "GAME_OVER":
                self.ui.draw_board(self.board, self.machine_pos, self.player_pos,
                                  self.destroyed, self.selected_pos, self.valid_moves)
                self.ui.draw_info_panel(self.difficulty, self.max_depth,
                                       self.machine_score, self.player_score,
                                       self.current_turn, self.game_over,
                                       self.machine_skipped, self.player_skipped)
                self.gameover_buttons = self.ui.draw_game_over(
                    self.winner, self.machine_score, self.player_score
                )
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()