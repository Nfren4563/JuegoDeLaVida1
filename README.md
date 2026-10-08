# Juego de la Vida

## Creador

Efren Alejandro Gonzalez  
GitHub: [Nfren4563](https://github.com/Nfren4563)

## Descripción

Este proyecto es una simulación del Juego de la Vida creado por Conway.

El programa utiliza un tablero de células. Cada célula puede estar viva o muerta y su estado cambia dependiendo de la cantidad de células vecinas que tenga.

El proyecto fue desarrollado en Python y funciona desde la terminal de Windows.

## Reglas

- Una célula viva con menos de dos vecinas muere.
- Una célula viva con dos o tres vecinas continúa viva.
- Una célula viva con más de tres vecinas muere.
- Una célula muerta con exactamente tres vecinas nace.

## Funciones principales

- Tablero de 80 × 80.
- Selección manual de células.
- Movimiento mediante flechas.
- Simulación automática.
- Contador de generaciones.
- Colores en la terminal.

## Requisitos

- Windows 10 u 11.
- Python 3.
- Terminal compatible con colores.

Este proyecto utiliza `msvcrt`, por lo que está diseñado para Windows.

## Cómo descargarlo

```bash
git clone https://github.com/Nfren4563/JuegoDeLaVida1.git
cd JuegoDeLaVida1/juegodelavida
```

## Ejecución

```bash
python juego.py
```

## Controles

| Tecla | Función |
|---|---|
| Flechas | Mover el cursor |
| Enter | Activar o desactivar una célula |
| Espacio | Iniciar la simulación |
| Q o Esc | Salir o detener la simulación |

## Imágenes

Por agregar...

## Configuración

El tamaño del tablero puede modificarse dentro de `juego.py`:

```python
FILAS = 80
COLS = 80
```

## Nota

Se recomienda maximizar la terminal para poder observar correctamente el tablero completo.

## Estado del proyecto

Proyecto terminado con fines educativos.
