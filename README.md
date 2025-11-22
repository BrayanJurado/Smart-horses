# 🐴 Smart Horses

Un juego de estrategia por turnos donde un jugador humano se enfrenta a una inteligencia artificial basada en el algoritmo **Minimax con poda alfa-beta**. Cada jugador controla un caballo de ajedrez en un tablero, buscando maximizar sus puntos mientras destruye casillas estratégicamente.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Descripción del Juego

Smart Horses es un juego para dos jugadores donde cada uno controla un caballo sobre un tablero de ajedrez de 8×8. El tablero incluye 10 casillas con puntos (positivos y negativos). En cada turno, un jugador debe mover su caballo a una nueva posición siguiendo las reglas de movimiento del ajedrez (movimiento en L).

### 🎯 Objetivos
- Acumular la mayor cantidad de puntos posible
- Capturar casillas con valores positivos
- Evitar casillas con valores negativos
- Bloquear estratégicamente a tu oponente
- Mantener movilidad para no recibir penalizaciones

### 📜 Reglas del Juego

1. **Movimientos**: Los caballos se mueven en forma de "L" como en el ajedrez (2 casillas en una dirección y 1 en perpendicular)

2. **Puntos**: Al llegar a una casilla con puntos, el jugador obtiene/pierde esa cantidad
   - Valores positivos: +1, +3, +4, +5, +10
   - Valores negativos: -1, -3, -4, -5, -10

3. **Destrucción de casillas**: Cada casilla donde se posiciona un caballo queda destruida y no puede ser usada nuevamente

4. **Penalización**: Si un jugador no tiene movimientos disponibles pero su oponente sí, recibe -4 puntos

5. **Fin del juego**: El juego termina cuando ninguno de los jugadores puede realizar un movimiento válido

6. **Victoria**: Gana el jugador con la mayor puntuación al finalizar la partida

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/BrayanJurado/Smart-horses.git
cd smart-horses
```

### Paso 2: Instalar Dependencias
```bash
pip install pygame
```

## 🎮 Cómo Jugar

### Iniciar el Juego
```bash
python main.py
```

### Selección de Dificultad
Al iniciar, selecciona uno de los tres niveles de dificultad:

- **🟢 Principiante** (Profundidad 2): IA evalúa 2 movimientos hacia adelante
- **🟡 Amateur** (Profundidad 4): IA evalúa 4 movimientos hacia adelante
- **🔴 Experto** (Profundidad 6): IA evalúa 6 movimientos hacia adelante

### Controles

| Acción | Control |
|--------|---------|
| Seleccionar caballo | Clic izquierdo en tu caballo (negro) |
| Mover caballo | Clic izquierdo en casilla resaltada |
| Deseleccionar | Clic derecho en cualquier parte |

### Flujo del Juego

1. **La máquina (caballo blanco) siempre inicia el juego**
2. Espera tu turno (jugador con caballo negro)
3. Haz clic en tu caballo para ver los movimientos disponibles (casillas resaltadas en verde)
4. Haz clic en una casilla válida para mover
5. La máquina calculará y ejecutará su mejor movimiento
6. Repite hasta que el juego termine

### Información en Pantalla

El panel lateral muestra:
- Nivel de dificultad actual
- Profundidad del árbol Minimax
- Puntuación de la Máquina (Blanco)
- Puntuación del Jugador (Negro)
- Turno actual
- Notificaciones de penalizaciones
- Instrucciones de control

## 🧠 Algoritmo de Inteligencia Artificial

### Minimax con Poda Alfa-Beta

La IA utiliza el algoritmo Minimax con poda alfa-beta para determinar el mejor movimiento posible. Este algoritmo:

1. **Explora el árbol de decisiones** hasta la profundidad configurada
2. **Evalúa estados futuros** usando una función heurística
3. **Optimiza la búsqueda** descartando ramas innecesarias (poda alfa-beta)
4. **Selecciona el movimiento óptimo** que maximiza su ventaja

### Función Heurística

La función de evaluación considera cuatro factores principales:

```
h(estado) = 1.0 × Δ_puntos + 0.3 × Δ_movilidad + 0.5 × Δ_alcanzables + 0.2 × control_centro
```

#### Componentes:

1. **Diferencia de Puntos (peso 1.0)**
   - Diferencia entre puntuación de la máquina y el jugador
   - Factor más importante: representa el objetivo principal del juego

2. **Diferencia de Movilidad (peso 0.3)**
   - Diferencia en cantidad de movimientos legales disponibles
   - Evita quedar sin opciones y recibir penalización de -4 puntos
   - Mantiene flexibilidad táctica

3. **Valor de Casillas Alcanzables (peso 0.5)**
   - Valor promedio de casillas con puntos alcanzables en 1-2 turnos
   - Movimientos inmediatos: peso completo
   - Movimientos futuros: peso 0.5
   - Permite planificación a medio plazo

4. **Control del Centro (peso 0.2)**
   - Ventaja posicional basada en distancia Manhattan al centro
   - Estar en el centro proporciona más opciones de movimiento
   - Factor táctico secundario

### Profundidad por Nivel

| Nivel | Profundidad | Complejidad |
|-------|-------------|-------------|
| Principiante | 2 | ~64 estados evaluados |
| Amateur | 4 | ~4,096 estados evaluados |
| Experto | 6 | ~262,144 estados evaluados |

*Valores aproximados considerando factor de ramificación promedio de 8 movimientos*

## 👥 Autores

- **Brayan Camilo Urrea Jurado** - [BrayanJurado](https://github.com/BrayanJurado)
- **Nicolás Enrique Granada Fernandez** - [NicolasGranada](https://github.com/NicolasGranada)

🐴 **¡Disfruta jugando Smart Horses!** 🐴
