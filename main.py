"""
Smart Horses - Juego de Estrategia con IA
Punto de entrada principal
"""
import pygame
import sys
from game import SmartHorsesGame

def main():
    """Función principal del juego"""
    try:
        pygame.init()
        game = SmartHorsesGame()
        game.run()
    except Exception as e:
        print(f"Error al ejecutar el juego: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()