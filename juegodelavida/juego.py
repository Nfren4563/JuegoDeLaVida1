from interaccion import *
import os
import time

FILAS = 80
COLS  = 80
 
COLOR_TITULO    = "0969da"  
COLOR_SUBTITULO = "eda73b"  
COLOR_TEXTO     = "8b9bb4"
COLOR_VIVA      = "0969da"
COLOR_CURSOR    = "9D00FF"
SIMBOLO_VIVA    = "■"
SIMBOLO_CURSOR  = "▓"
SIMBOLO_MUERTA  = " "

OFFSET_FILA = 6
OFFSET_COL = 2


def mostrar_titulo():
    cls_limpiar_pantalla()
 
    cls_mover_cursor(1, 1)
    cls_establecer_color_hex(COLOR_TITULO)
    cls_imprimir("=" * 50)
 
    cls_mover_cursor(2, 1)
    cls_establecer_color_hex(COLOR_TITULO)
    cls_imprimir("░░ EL JUEGO DE LA VIDA ░░")
 
    cls_mover_cursor(3, 1)
    cls_establecer_color_hex(COLOR_SUBTITULO)
    cls_imprimir("   EFREN ALEJANDRO GONZALEZ")
 
    cls_mover_cursor(4, 1)
    cls_establecer_color_hex(COLOR_TITULO)
    cls_imprimir("=" * 50)
 
    cls_mover_cursor(5, 1)
    cls_establecer_color_hex(COLOR_SUBTITULO)
    cls_imprimir("Presiona cualquier tecla para continuar...")
 
    cls_restaurar_colores()
    cls_leer_tecla()

def crear_tablero():
    tablero = []
    for f in range(FILAS):
        fila = []
        for c in range(COLS):
            fila.append(False)
        tablero.append(fila)
    return tablero

def dibujar_celula(fila,col,viva):
    fila_visual = fila + OFFSET_FILA
    col_visual = col + OFFSET_COL

    cls_mover_cursor(fila_visual,col_visual)

    if viva:
        cls_establecer_color_hex(COLOR_VIVA)
        cls_imprimir(SIMBOLO_VIVA)
        cls_restaurar_colores()
    else:
        cls_imprimir(SIMBOLO_MUERTA)

def dibujar_cursor(fila,col):
    fila_visual = fila + OFFSET_FILA
    col_visual = col + OFFSET_COL
    cls_mover_cursor(fila_visual,col_visual)
    cls_establecer_color_hex(COLOR_CURSOR)
    cls_imprimir(SIMBOLO_CURSOR)
    cls_restaurar_colores()

def borrar_cursor(fila,col,tablero):
    dibujar_celula(fila,col,tablero[fila][col])

def dibujar_encabezado():
    cls_mover_cursor(1,1)
    cls_establecer_color_hex(COLOR_TITULO)
    cls_imprimir("░░ EL JUEGO DE LA VIDA ░░")

    cls_establecer_color_hex(COLOR_SUBTITULO)
    cls_imprimir("EFREN ALEJANDRO GONZALEZ")

    cls_mover_cursor(2,1)
    cls_establecer_color_hex(COLOR_TEXTO)
    cls_imprimir("Flechas: mover  |  ENTER: activar celula  |  ESPACIO: simular  |  Q: salir")

    cls_mover_cursor(3,1)
    cls_establecer_color_hex(COLOR_TITULO)
    cls_imprimir("-"*82)

    cls_restaurar_colores()

def fase_edicion(tablero):
    cls_limpiar_pantalla()
    dibujar_encabezado()

    cursor_fila = FILAS // 2
    cursor_col = COLS // 2

    dibujar_cursor(cursor_fila,cursor_col)

    cls_mover_cursor(4,1)
    cls_establecer_color_hex(COLOR_TEXTO)
    cls_imprimir(f"Cursor: ({cursor_fila}, {cursor_col})   ")
    cls_restaurar_colores()

    while True:
        tecla = cls_leer_tecla()

        if tecla == "SALIR":
            return False
            
        if tecla == "OTRA":
            return True
        
        if tecla == "ENTER":
            borrar_cursor(cursor_fila, cursor_col, tablero)
            tablero[cursor_fila][cursor_col] = not tablero[cursor_fila][cursor_col]
            dibujar_celula(cursor_fila, cursor_col, tablero[cursor_fila][cursor_col])
            dibujar_cursor(cursor_fila, cursor_col)
            continue

        fila_ant = cursor_fila
        col_ant  = cursor_col
 
        if tecla == "ARRIBA":
            cursor_fila = max(0, cursor_fila - 1)
        elif tecla == "ABAJO":
            cursor_fila = min(FILAS - 1, cursor_fila + 1)
        elif tecla == "DERECHA":
            cursor_col = min(COLS - 1, cursor_col + 1)
        elif tecla == "IZQUIERDA":
            cursor_col = max(0, cursor_col - 1)
 
        if fila_ant != cursor_fila or col_ant != cursor_col:
            borrar_cursor(fila_ant, col_ant, tablero)
            dibujar_cursor(cursor_fila, cursor_col)
 
            cls_mover_cursor(4, 1)
            cls_establecer_color_hex(COLOR_TEXTO)
            cls_imprimir(f"Cursor: ({cursor_fila}, {cursor_col})   ")
            cls_restaurar_colores()

def contar_vecinos(tablero,fila,col):
    vecinos = 0
    for df in [-1,0,1]:
        for dc in [-1,0,1]:
            if df == 0 and dc == 0:
                continue

            nf = (fila + df) % FILAS
            nc = (col + dc) % COLS
            if tablero[nf][nc]:
                vecinos += 1
    return vecinos

def siguiente_generacion(tablero):
    nuevo = crear_tablero()

    for f in range (FILAS):
        for c in range(COLS):
            v = contar_vecinos(tablero,f,c)

            if tablero[f][c]:
                nuevo[f][c] = v in (2,3)
            else:
                nuevo[f][c] = v == 3
    return nuevo

def redibujar_cambio(viejo,nuevo):
    for f in range(FILAS):
        for c in range(COLS):
            if viejo[f][c] != nuevo[f][c]:
                dibujar_celula(f,c,nuevo[f][c])

def fase_simulacion(tablero):
    generacion = 0
    cls_limpiar_pantalla()

    cls_mover_cursor(1, 1)
    cls_establecer_color_hex(COLOR_TITULO)
    cls_imprimir("░░ SIMULACION EN CURSO ░░  |  ")
    cls_establecer_color_hex(COLOR_SUBTITULO)
    cls_imprimir("EFREN ALEJANDRO GONZALEZ")
 
    cls_mover_cursor(2, 1)
    cls_establecer_color_hex(COLOR_TEXTO)
    cls_imprimir("Q: detener simulacion")
 
    cls_mover_cursor(3, 1)
    cls_establecer_color_hex(COLOR_TITULO)
    cls_imprimir("-" * 82)
    cls_restaurar_colores()

    for f in range(FILAS):
        for c in range(COLS):
            if tablero[f][c]:
                dibujar_celula(f,c,True)

    while True:
        if msvcrt.kbhit():
            tecla = cls_leer_tecla()
            if tecla == "SALIR":
                break

        nuevo_tablero = siguiente_generacion(tablero)

        redibujar_cambio(tablero,nuevo_tablero)
        tablero = nuevo_tablero
        generacion += 1

        cls_mover_cursor(4,1)
        cls_establecer_color_hex(COLOR_TEXTO)
        cls_imprimir(f"Generacion: {generacion}   ")
        cls_restaurar_colores()
 
        time.sleep(0.1)


def iniciar():
    os.system("")
    
    cls_ocultar_cursor()

 
    try:
        mostrar_titulo()
 
        tablero = crear_tablero()
         
        continuar = fase_edicion(tablero)

        if continuar:
            fase_simulacion(tablero)
 
    finally:
        cls_restaurar_colores()
        cls_mostrar_cursor()
        cls_mover_cursor(10, 1)
        print("Juego cerrado.")
 
if __name__ == "__main__":
    iniciar()