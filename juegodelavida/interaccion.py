import sys
import msvcrt
import os
import random  # ¡NUEVO! Importamos random para elegir colores al azar

# ==========================================
# CONFIGURACIÓN Y ESTILOS
# ==========================================

# Símbolos visuales.
SIMBOLO_SUELO = "■"
SIMBOLO_JUGADOR = "≡"

# Lista de colores.
COLORES_HEX = ["0969da", "eda73b", "8b9bb4", "e43b44"]

# ==========================================
# COMANDOS DE CONSOLA
# ==========================================

def cls_imprimir(texto):
    """Imprime texto inmediatamente en pantalla sin hacer salto de línea."""
    sys.stdout.write(texto)
    sys.stdout.flush()

def cls_mover_cursor(fila, columna):
    """Mueve el cursor a una posición específica de la terminal."""
    cls_imprimir(f"\033[{fila};{columna}H")

def cls_ocultar_cursor():
    """Oculta el cursor parpadeante."""
    cls_imprimir("\033[?25l")

def cls_mostrar_cursor():
    """Muestra nuevamente el cursor."""
    cls_imprimir("\033[?25h")

def cls_limpiar_pantalla():
    """Borra todo el contenido de la consola."""
    cls_imprimir("\033[2J\033[H")

def cls_restaurar_colores():
    """Vuelve a los colores por defecto de la terminal."""
    cls_imprimir("\033[0m")

def cls_establecer_color_hex(hex_color):
    """
    Toma un color hexadecimal y aplica color 'True Color' (24 bits)
    al texto de la consola usando el código ANSI: \033[38;2;R;G;Bm
    """
    # 1. Convertir Hex (base 16) a RGB (base 10).
    # [0:2] toma los primeros dos caracteres, int(..., 16) lo convierte a entero base 10
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # 2. Aplicar el código ANSI True Color.
    cls_imprimir(f"\033[38;2;{r};{g};{b}m")

def cls_leer_tecla():
    """
    Lee la tecla y la traduce.
    """
    if not msvcrt.kbhit(): # Esperar a que el usuario presione alguna tecla.
        pass 
    
    tecla = msvcrt.getch()

    # Detectar ENTER.
    if tecla == b'\r':
        return "ENTER"

    # Detectar Flechas (son códigos de dos bytes).
    if tecla in (b'\x00', b'\xe0'):
        flecha = msvcrt.getch()
        if flecha == b'H': return "ARRIBA"
        if flecha == b'P': return "ABAJO"
        if flecha == b'M': return "DERECHA"
        if flecha == b'K': return "IZQUIERDA"

    # Detectar SALIR.
    if tecla.lower() == b'q' or tecla == b'\x1b':
        return "SALIR"

    return "OTRA"

# ==========================================
# LÓGICA DEL JUEGO
# ==========================================

def dibujar_tablero():
    """Dibuja la cuadrícula vacía."""
    cls_limpiar_pantalla()
    # Asegurar que el suelo se dibuje con el color por defecto
    cls_restaurar_colores() 
    for _ in range(5):
        print(f"{SIMBOLO_SUELO} " * 5)

def dibujar_personaje(fila, columna, color_hex):
    """Calcula la posición visual, aplica el color y dibuja al personaje."""
    columna_visual = (columna * 2) - 1
    cls_mover_cursor(fila, columna_visual)
    
    # 1. Activamos el color especial antes de imprimir.
    cls_establecer_color_hex(color_hex)
    
    # 2. Imprimimos el personaje.
    cls_imprimir(SIMBOLO_JUGADOR)
    
    # 3. Es importante restaurar colores inmediatamente para no "pintar" el resto de los caracteres en consola.
    cls_restaurar_colores()

def borrar_rastro(fila, columna):
    """Dibuja un bloque de suelo normal donde estaba el personaje."""
    columna_visual = (columna * 2) - 1
    cls_mover_cursor(fila, columna_visual)
    cls_restaurar_colores() # Asegurar color por defecto para el suelo
    cls_imprimir(SIMBOLO_SUELO)

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def iniciar_juego():
    # Preparación
    os.system("") 
    cls_ocultar_cursor()
    
    # Estado inicial
    fila = 1
    columna = 1
    # Elegimos un color inicial aleatorio de la lista
    color_actual = random.choice(COLORES_HEX)
    
    dibujar_tablero()
    dibujar_personaje(fila, columna, color_actual)

    cls_mover_cursor(7, 1)
    print("Controles: Flechas (Mover), ENTER (Cambiar Color), Q (Salir)")

    try:
        while True:
            comando = cls_leer_tecla()

            if comando == "SALIR":
                break
            
            # LÓGICA DEL COLOR.
            if comando == "ENTER":
                # Elegimos un nuevo color aleatorio.
                nuevo_color = random.choice(COLORES_HEX)
                # Opcional: Asegurar que el color sea diferente al actual.
                while nuevo_color == color_actual:
                    nuevo_color = random.choice(COLORES_HEX)
                
                color_actual = nuevo_color
                # Volvemos a dibujar el personaje en el mismo lugar pero con nuevo color.
                dibujar_personaje(fila, columna, color_actual)
                continue # Saltamos el resto del ciclo.

            # LÓGICA DE MOVIMIENTO.
            fila_ant, col_ant = fila, columna

            if comando == "ARRIBA":
                fila = max(1, fila - 1)
            elif comando == "ABAJO":
                fila = min(5, fila + 1)
            elif comando == "DERECHA":
                columna = min(5, columna + 1)
            elif comando == "IZQUIERDA": 
                columna = max(1, columna - 1)

            if fila != fila_ant or columna != col_ant:
                borrar_rastro(fila_ant, col_ant)
                dibujar_personaje(fila, columna, color_actual)

    finally:
        # Limpieza final.
        cls_restaurar_colores() # Importante: quitar colores antes de salir.
        cls_mostrar_cursor()
        cls_mover_cursor(9, 1)
        print("Juego cerrado.")

if __name__ == "__main__":
    iniciar_juego()