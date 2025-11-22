"""
Algoritmo Minimax con poda alfa-beta y función heurística
"""
from typing import Tuple, Optional

class MinimaxAI:
    """IA basada en Minimax para Smart Horses"""
    
    def __init__(self, board_size: int = 8):
        self.board_size = board_size
    
    def get_valid_moves(self, pos: Tuple[int, int], destroyed: set) -> list:
        """Obtiene movimientos válidos del caballo"""
        row, col = pos
        moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]
        
        return [(r, c) for r, c in moves 
                if 0 <= r < self.board_size and 
                0 <= c < self.board_size and 
                (r, c) not in destroyed]
    
    def calculate_reachable_value(self, pos: Tuple[int, int], 
                                  destroyed: set, board: list) -> float:
        """Calcula el valor de casillas alcanzables en 1-2 movimientos"""
        total_value = 0
        moves_1 = self.get_valid_moves(pos, destroyed)
        
        for move1 in moves_1:
            cell_value = board[move1[0]][move1[1]]
            if isinstance(cell_value, int):
                total_value += cell_value
            
            temp_destroyed = destroyed.copy()
            temp_destroyed.add(move1)
            moves_2 = self.get_valid_moves(move1, temp_destroyed)
            
            for move2 in moves_2:
                cell_value = board[move2[0]][move2[1]]
                if isinstance(cell_value, int):
                    total_value += cell_value * 0.5
        
        return total_value / max(len(moves_1), 1)
    
    def heuristic(self, machine_pos, player_pos, destroyed, 
                  machine_score, player_score, board) -> float:
        """
        Función heurística para evaluar estados del juego.
        
        h(estado) = 1.0 x Δ_puntos + 0.3 x Δ_movilidad + 
                    0.5 x Δ_alcanzables + 0.2 x control_centro
        """
        # 1. Diferencia de puntuación
        score_diff = machine_score - player_score
        
        # 2. Diferencia de movilidad
        machine_moves = self.get_valid_moves(machine_pos, destroyed)
        player_moves = self.get_valid_moves(player_pos, destroyed)
        mobility_diff = len(machine_moves) - len(player_moves)
        
        # 3. Diferencia de casillas alcanzables
        machine_reachable = self.calculate_reachable_value(machine_pos, destroyed, board)
        player_reachable = self.calculate_reachable_value(player_pos, destroyed, board)
        reachable_diff = machine_reachable - player_reachable
        
        # 4. Control del centro
        center = self.board_size / 2
        machine_center_dist = abs(machine_pos[0] - center) + abs(machine_pos[1] - center)
        player_center_dist = abs(player_pos[0] - center) + abs(player_pos[1] - center)
        center_control = player_center_dist - machine_center_dist
        
        return (1.0 * score_diff + 0.3 * mobility_diff + 
                0.5 * reachable_diff + 0.2 * center_control)
    
    def minimax(self, depth: int, is_maximizing: bool, alpha: float, beta: float,
                machine_pos, player_pos, destroyed: set,
                machine_score: int, player_score: int, board: list):
        """Algoritmo Minimax con poda alfa-beta"""
        
        if is_maximizing:
            moves = self.get_valid_moves(machine_pos, destroyed)
        else:
            moves = self.get_valid_moves(player_pos, destroyed)
        
        # Condición de terminación
        if depth == 0 or len(moves) == 0:
            final_machine_score = machine_score
            final_player_score = player_score
            
            # Aplicar penalización si corresponde
            if depth > 0 and len(moves) == 0:
                if is_maximizing:
                    other_moves = self.get_valid_moves(player_pos, destroyed)
                    if len(other_moves) > 0:
                        final_machine_score -= 4
                else:
                    other_moves = self.get_valid_moves(machine_pos, destroyed)
                    if len(other_moves) > 0:
                        final_player_score -= 4
            
            return self.heuristic(machine_pos, player_pos, destroyed,
                                final_machine_score, final_player_score, board), None
        
        best_move = None
        
        if is_maximizing:
            # Nodo MAX (máquina)
            max_eval = float('-inf')
            for move in moves:
                new_destroyed = destroyed.copy()
                new_destroyed.add(machine_pos)
                
                points = 0
                cell_value = board[move[0]][move[1]]
                if isinstance(cell_value, int):
                    points = cell_value
                
                eval_score, _ = self.minimax(depth - 1, False, alpha, beta,
                                            move, player_pos, new_destroyed,
                                            machine_score + points, player_score, board)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            
            return max_eval, best_move
        else:
            # Nodo MIN (jugador)
            min_eval = float('inf')
            for move in moves:
                new_destroyed = destroyed.copy()
                new_destroyed.add(player_pos)
                
                points = 0
                cell_value = board[move[0]][move[1]]
                if isinstance(cell_value, int):
                    points = cell_value
                
                eval_score, _ = self.minimax(depth - 1, True, alpha, beta,
                                            machine_pos, move, new_destroyed,
                                            machine_score, player_score + points, board)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            
            return min_eval, best_move
    
    def get_best_move(self, machine_pos, player_pos, destroyed: set,
                     machine_score: int, player_score: int, 
                     board: list, depth: int):
        """Obtiene el mejor movimiento para la máquina"""
        _, best_move = self.minimax(depth, True, float('-inf'), float('inf'),
                                    machine_pos, player_pos, destroyed,
                                    machine_score, player_score, board)
        return best_move