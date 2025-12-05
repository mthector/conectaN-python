# ConectaN - Juego de tablero configurable
# Autor: Héctor Tudela Morales
# IES Zaidín-Vergeles
# Desarrollo de aplicaciones en lenguaje Python

# Este módulo se utiliza para generar comportamientos aleatorios en la inteligencia artificial del juego.
import random
import os


# ============================================================================
# CONSTANTES DEL JUEGO
# ============================================================================

# Constantes para representar el estado de las casillas del tablero
CASILLA_VACIA = 0
FICHA_CIRCULO = 1
FICHA_EQUIS = 2

# Códigos de color ANSI para la terminal (mejora la experiencia visual)
COLOR_RESET = "\033[0m"
COLOR_CIRCULO = "\033[94m"  # Azul para jugador O
COLOR_EQUIS = "\033[91m"    # Rojo para jugador X
COLOR_ULTIMA = "\033[93m"   # Amarillo para resaltar última ficha


# ============================================================================
# FUNCIONES DE GESTIÓN DEL TABLERO
# ============================================================================

def crear_tablero(filas, columnas):
    """
    Crea un tablero vacío con el tamaño especificado.
    Valida que el tamaño sea al menos 6x7 según las especificaciones.
    
    Args:
        filas (int): Número de filas del tablero (mínimo 6)
        columnas (int): Número de columnas del tablero (mínimo 7)
    
    Returns:
        list: Matriz (lista de listas) inicializada con CASILLA_VACIA,
              o None si los parámetros no son válidos
    """
    # Validación de parámetros de entrada
    if not isinstance(filas, int) or not isinstance(columnas, int):
        return None
    if filas < 6 or columnas < 7:
        return None
    
    # Crear matriz con list comprehension (más eficiente que bucles anidados)
    return [[CASILLA_VACIA for _ in range(columnas)] for _ in range(filas)]


def mostrar_tablero(tablero):
    """
    Muestra el tablero en la consola con colores para las fichas.
    Representa las fichas con símbolos O y X coloreados.
    
    Args:
        tablero (list): Matriz que representa el tablero del juego
    """
    # Validación del parámetro
    if not tablero or not isinstance(tablero, list):
        return
    
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0
    
    # Mostrar números de columna (1-indexed para el usuario)
    print("\n  ", end="")
    for col in range(columnas):
        print(f"{col + 1:^4}", end="")
    print()
    
    # Mostrar cada fila del tablero con sus fichas coloreadas
    for fila in range(filas):
        print("  |", end="")
        for col in range(columnas):
            if tablero[fila][col] == CASILLA_VACIA:
                print("   |", end="")
            elif tablero[fila][col] == FICHA_CIRCULO:
                print(f" {COLOR_CIRCULO}O{COLOR_RESET} |", end="")
            elif tablero[fila][col] == FICHA_EQUIS:
                print(f" {COLOR_EQUIS}X{COLOR_RESET} |", end="")
        print()
    
    # Línea inferior del tablero
    print("  " + "----" * columnas)


def mostrar_tablero_columna(tablero, columna_ultima_ficha):
    """
    Muestra el tablero resaltando la última ficha colocada en color amarillo.
    Esta función mejora la experiencia de usuario al visualizar el último movimiento.
    
    Args:
        tablero (list): Matriz que representa el tablero del juego
        columna_ultima_ficha (int): Columna donde se colocó la última ficha (0-indexed)
    """
    # Validación exhaustiva de parámetros
    if not tablero or not isinstance(tablero, list):
        return
    if not isinstance(columna_ultima_ficha, int):
        return
    if columna_ultima_ficha < 0 or columna_ultima_ficha >= len(tablero[0]):
        return
    
    filas = len(tablero)
    columnas = len(tablero[0])
    
    # Encontrar la fila de la última ficha colocada (busca desde abajo)
    fila_ultima = -1
    for fila in range(filas - 1, -1, -1):
        if tablero[fila][columna_ultima_ficha] != CASILLA_VACIA:
            fila_ultima = fila
            break
    
    # Mostrar números de columna
    print("\n  ", end="")
    for col in range(columnas):
        print(f"{col + 1:^4}", end="")
    print()
    
    # Mostrar tablero con la última ficha resaltada
    for fila in range(filas):
        print("  |", end="")
        for col in range(columnas):
            if tablero[fila][col] == CASILLA_VACIA:
                print("   |", end="")
            elif fila == fila_ultima and col == columna_ultima_ficha:
                # Resaltar última ficha en amarillo
                simbolo = "O" if tablero[fila][col] == FICHA_CIRCULO else "X"
                print(f" {COLOR_ULTIMA}{simbolo}{COLOR_RESET} |", end="")
            elif tablero[fila][col] == FICHA_CIRCULO:
                print(f" {COLOR_CIRCULO}O{COLOR_RESET} |", end="")
            elif tablero[fila][col] == FICHA_EQUIS:
                print(f" {COLOR_EQUIS}X{COLOR_RESET} |", end="")
        print()
    
    # Línea inferior
    print("  " + "----" * columnas)


def colocar_ficha(tablero, ficha, columna):
    """
    Coloca una ficha en la columna especificada, simulando la caída por gravedad.
    La ficha se coloca en la posición más baja disponible de la columna.
    
    Args:
        tablero (list): Matriz que representa el tablero del juego
        ficha (int): Tipo de ficha (FICHA_CIRCULO o FICHA_EQUIS)
        columna (int): Columna donde colocar la ficha (0-indexed)
    
    Returns:
        bool: True si se colocó exitosamente, False si no fue posible
    """
    # Validación completa de parámetros
    if not tablero or not isinstance(tablero, list):
        return False
    if not isinstance(columna, int):
        return False
    if columna < 0 or columna >= len(tablero[0]):
        return False
    if ficha not in [FICHA_CIRCULO, FICHA_EQUIS]:
        return False
    
    filas = len(tablero)
    
    # Buscar la fila más baja disponible (simula gravedad)
    for fila in range(filas - 1, -1, -1):
        if tablero[fila][columna] == CASILLA_VACIA:
            tablero[fila][columna] = ficha
            return True
    
    # Si llegamos aquí, la columna está llena
    return False


# ============================================================================
# FUNCIONES DE COMPROBACIÓN DE VICTORIAS
# ============================================================================

def contar_fichas_direccion(tablero, fila, columna, ficha, dir_fila, dir_col):
    """
    Cuenta cuántas fichas consecutivas hay en una dirección específica.
    Esta función auxiliar es usada para detectar líneas ganadoras.
    
    Args:
        tablero (list): Matriz que representa el tablero
        fila (int): Fila inicial desde donde contar
        columna (int): Columna inicial desde donde contar
        ficha (int): Tipo de ficha a contar
        dir_fila (int): Dirección en filas (-1, 0, 1)
        dir_col (int): Dirección en columnas (-1, 0, 1)
    
    Returns:
        int: Número de fichas consecutivas en la dirección especificada
    """
    # Validación de parámetros
    if not tablero or not isinstance(tablero, list):
        return 0
    
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0
    contador = 0
    
    # Avanzar en la dirección especificada contando fichas
    fila_actual = fila + dir_fila
    col_actual = columna + dir_col
    
    while (0 <= fila_actual < filas and 0 <= col_actual < columnas and
           tablero[fila_actual][col_actual] == ficha):
        contador += 1
        fila_actual += dir_fila
        col_actual += dir_col
    
    return contador


def comprobar_linea(tablero, columna, numero_fichas_linea):
    """
    Comprueba si hay una línea ganadora desde la última ficha colocada.
    Verifica las 4 direcciones posibles: horizontal, vertical y 2 diagonales.
    
    Args:
        tablero (list): Matriz que representa el tablero
        columna (int): Columna de la última ficha colocada
        numero_fichas_linea (int): Número de fichas necesarias para ganar
    
    Returns:
        bool: True si hay línea ganadora, False en caso contrario
    """
    # Validación exhaustiva de parámetros
    if not tablero or not isinstance(tablero, list):
        return False
    if not isinstance(columna, int) or not isinstance(numero_fichas_linea, int):
        return False
    if columna < 0 or columna >= len(tablero[0]):
        return False
    if numero_fichas_linea < 1:
        return False
    
    filas = len(tablero)
    
    # Encontrar la fila de la última ficha en la columna especificada
    fila = -1
    for f in range(filas):
        if tablero[f][columna] != CASILLA_VACIA:
            fila = f
            break
    
    # Si no hay ficha en esa columna, no puede haber victoria
    if fila == -1:
        return False
    
    ficha = tablero[fila][columna]
    
    # Direcciones a comprobar: horizontal, vertical, diagonal \, diagonal /
    direcciones = [
        (0, 1),   # Horizontal (derecha-izquierda)
        (1, 0),   # Vertical (arriba-abajo)
        (1, 1),   # Diagonal \ (descendente)
        (1, -1)   # Diagonal / (ascendente)
    ]
    
    # Comprobar cada dirección
    for dir_fila, dir_col in direcciones:
        # Contar en ambas direcciones y sumar 1 por la ficha actual
        total = 1  # La ficha que acabamos de colocar
        total += contar_fichas_direccion(tablero, fila, columna, ficha, dir_fila, dir_col)
        total += contar_fichas_direccion(tablero, fila, columna, ficha, -dir_fila, -dir_col)
        
        # Si encontramos suficientes fichas en línea, hay victoria
        if total >= numero_fichas_linea:
            return True
    
    return False


def fichas_en_linea(tablero, ficha, columna):
    """
    Calcula el máximo de fichas en línea que se obtendrían al colocar una ficha.
    Esta función simula la colocación sin modificar el tablero permanentemente.
    Es crucial para la estrategia de la IA nivel 2.
    
    Args:
        tablero (list): Matriz que representa el tablero
        ficha (int): Tipo de ficha a simular
        columna (int): Columna donde simular la colocación
    
    Returns:
        int: Número máximo de fichas en línea que se obtendrían
    """
    # Validación de parámetros
    if not tablero or not isinstance(tablero, list):
        return 0
    if not isinstance(columna, int) or not isinstance(ficha, int):
        return 0
    if columna < 0 or columna >= len(tablero[0]):
        return 0
    if ficha not in [FICHA_CIRCULO, FICHA_EQUIS]:
        return 0
    
    filas = len(tablero)
    
    # Encontrar dónde caería la ficha (simulación de gravedad)
    fila = -1
    for f in range(filas - 1, -1, -1):
        if tablero[f][columna] == CASILLA_VACIA:
            fila = f
            break
    
    # Si la columna está llena, no se puede colocar
    if fila == -1:
        return 0
    
    # Simular temporalmente la colocación de la ficha
    tablero[fila][columna] = ficha
    
    # Direcciones a verificar
    direcciones = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1)   # Diagonal /
    ]
    
    # Calcular el máximo en todas las direcciones
    maximo = 0
    for dir_fila, dir_col in direcciones:
        total = 1
        total += contar_fichas_direccion(tablero, fila, columna, ficha, dir_fila, dir_col)
        total += contar_fichas_direccion(tablero, fila, columna, ficha, -dir_fila, -dir_col)
        maximo = max(maximo, total)
    
    # Deshacer la simulación (muy importante para no alterar el tablero)
    tablero[fila][columna] = CASILLA_VACIA
    
    return maximo


def hay_casillas_libres(tablero):
    """
    Verifica si quedan casillas libres en el tablero.
    Se usa para detectar situaciones de empate.
    
    Args:
        tablero (list): Matriz que representa el tablero
    
    Returns:
        bool: True si hay casillas libres, False si el tablero está completo
    """
    # Validación del parámetro
    if not tablero or not isinstance(tablero, list):
        return False
    
    # Buscar cualquier casilla vacía en el tablero
    for fila in tablero:
        if CASILLA_VACIA in fila:
            return True
    
    return False


# ============================================================================
# FUNCIONES AUXILIARES PARA COLUMNAS
# ============================================================================

def columna_esta_disponible(tablero, columna):
    """
    Verifica si una columna tiene espacio disponible en la parte superior.
    
    Args:
        tablero (list): Matriz que representa el tablero
        columna (int): Columna a verificar (0-indexed)
    
    Returns:
        bool: True si la columna está disponible, False si está llena
    """
    # Validación de parámetros
    if not tablero or not isinstance(tablero, list):
        return False
    if not isinstance(columna, int):
        return False
    if columna < 0 or columna >= len(tablero[0]):
        return False
    
    # Una columna está disponible si su primera fila está vacía
    return tablero[0][columna] == CASILLA_VACIA


def obtener_columnas_disponibles(tablero):
    """
    Obtiene una lista con los índices de todas las columnas disponibles.
    Útil para la IA al decidir movimientos válidos.
    
    Args:
        tablero (list): Matriz que representa el tablero
    
    Returns:
        list: Lista de índices de columnas disponibles
    """
    if not tablero or not isinstance(tablero, list):
        return []
    
    columnas = len(tablero[0]) if len(tablero) > 0 else 0
    
    # Usar list comprehension para eficiencia
    return [col for col in range(columnas) if columna_esta_disponible(tablero, col)]


# ============================================================================
# INTELIGENCIA ARTIFICIAL (IA)
# ============================================================================

def ia_nivel_1(tablero):
    """
    IA nivel 1: Selecciona una columna aleatoria entre las disponibles.
    Este nivel proporciona un desafío básico para jugadores principiantes.
    
    Args:
        tablero (list): Matriz que representa el tablero
    
    Returns:
        int: Índice de columna seleccionada, o -1 si no hay movimientos posibles
    """
    columnas_disponibles = obtener_columnas_disponibles(tablero)
    
    if columnas_disponibles:
        return random.choice(columnas_disponibles)
    
    return -1


def ia_nivel_2(tablero, ficha_ia, ficha_jugador, numero_fichas_linea):
    """
    IA nivel 2: Aplica estrategia avanzada con prioridades.
    
    Reglas en orden de prioridad:
    1. Ganar si es posible (colocar ficha que complete N en línea)
    2. Bloquear al jugador si está a punto de ganar
    3. Maximizar el número de fichas en línea propias
    4. Movimiento aleatorio si no aplican las anteriores
    
    Args:
        tablero (list): Matriz que representa el tablero
        ficha_ia (int): Tipo de ficha de la IA
        ficha_jugador (int): Tipo de ficha del jugador humano
        numero_fichas_linea (int): Número de fichas necesarias para ganar
    
    Returns:
        int: Índice de columna seleccionada, o -1 si no hay movimientos posibles
    """
    columnas_disponibles = obtener_columnas_disponibles(tablero)
    
    if not columnas_disponibles:
        return -1
    
    # REGLA 1: Ganar si es posible (máxima prioridad)
    for col in columnas_disponibles:
        if fichas_en_linea(tablero, ficha_ia, col) >= numero_fichas_linea:
            return col
    
    # REGLA 2: Bloquear al jugador si va a ganar en su próximo turno
    for col in columnas_disponibles:
        if fichas_en_linea(tablero, ficha_jugador, col) >= numero_fichas_linea:
            return col
    
    # REGLA 3: Maximizar fichas en línea de la IA
    mejor_columna = []
    max_fichas = 0
    
    for col in columnas_disponibles:
        fichas = fichas_en_linea(tablero, ficha_ia, col)
        if fichas > max_fichas:
            max_fichas = fichas
            mejor_columna = [col]
        elif fichas == max_fichas:
            mejor_columna.append(col)
    
    # Si hay columnas que maximizan fichas, elegir una aleatoriamente
    if mejor_columna and max_fichas > 0:
        return random.choice(mejor_columna)
    
    # REGLA 4: Movimiento aleatorio como último recurso
    return random.choice(columnas_disponibles)


# ============================================================================
# FUNCIONES DE INTERACCIÓN CON EL USUARIO
# ============================================================================

def solicitar_numero(mensaje, minimo, maximo):
    """
    Solicita un número al usuario con validación robusta.
    Maneja errores de entrada y valida rangos.
    
    Args:
        mensaje (str): Mensaje a mostrar al usuario
        minimo (int): Valor mínimo aceptable (inclusivo)
        maximo (int): Valor máximo aceptable (inclusivo)
    
    Returns:
        int: Número válido ingresado por el usuario
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"Por favor, ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número entero.")
        except KeyboardInterrupt:
            print("\nInterrupción detectada. Saliendo...")
            exit(0)


def limpiar_pantalla():
    """
    Limpia la pantalla de la consola para mejorar la experiencia visual.
    Compatible con Windows (cls) y Unix/Linux/Mac (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def preguntar_jugar_otra_vez():
    """
    Pregunta al usuario si desea jugar otra partida.
    
    Returns:
        bool: True si desea jugar de nuevo, False si desea salir
    """
    while True:
        print("\n¿Deseas jugar otra partida?")
        print("1. Sí, jugar de nuevo")
        print("2. No, salir del juego")
        opcion = solicitar_numero("Selecciona una opción: ", 1, 2)
        
        if opcion == 1:
            return True
        else:
            return False


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """
    Función principal del juego ConectaN.
    
    Gestiona el flujo completo del juego:
    - Configuración inicial (tamaño tablero, modo juego, jugadores)
    - Bucle principal de la partida
    - Alternancia de turnos
    - Detección de victoria o empate
    - Opción de jugar múltiples partidas
    """
    jugar_de_nuevo = True
    
    # Bucle para permitir múltiples partidas
    while jugar_de_nuevo:
        limpiar_pantalla()
        
        # Cabecera del juego
        print("=" * 50)
        print("       BIENVENIDO AL JUEGO CONECTA N")
        print("       HÉCTOR TUDELA MORALES")
        print("       IES ZAIDÍN VERGELES")
        print("=" * 50)
        
        # ========== CONFIGURACIÓN DEL TABLERO ==========
        print("\nCONFIGURACIÓN DEL TABLERO")
        print("El tablero debe tener mínimo 6 filas y 7 columnas.")
        
        filas = solicitar_numero("Número de filas: ", 6, 20)
        columnas = solicitar_numero("Número de columnas: ", 7, 20)
        
        # Crear tablero con validación
        tablero = crear_tablero(filas, columnas)
        if not tablero:
            print("Error: No se pudo crear el tablero con los parámetros especificados.")
            return
        
        # ========== CONFIGURACIÓN DE FICHAS PARA GANAR ==========
        max_fichas = min(filas, columnas)
        print(f"\nNúmero de fichas en línea para ganar")
        print(f"(mínimo 4, máximo {max_fichas}): ")
        numero_fichas_linea = solicitar_numero("", 4, max_fichas)
        
        # ========== SELECCIÓN DE MODO DE JUEGO ==========
        print("\nMODO DE JUEGO:")
        print("1. Jugador vs Jugador")
        print("2. Jugador vs IA")
        modo_juego = solicitar_numero("Selecciona el modo de juego: ", 1, 2)
        
        # ========== CONFIGURACIÓN DE JUGADORES ==========
        nombre_jugador1 = input("\nNombre del Jugador 1 (O): ").strip()
        if not nombre_jugador1:
            nombre_jugador1 = "Jugador 1"
        
        # Configuración específica según el modo
        if modo_juego == 1:
            # Modo Jugador vs Jugador
            nombre_jugador2 = input("Nombre del Jugador 2 (X): ").strip()
            if not nombre_jugador2:
                nombre_jugador2 = "Jugador 2"
            nivel_ia = None
        else:
            # Modo Jugador vs IA
            nombre_jugador2 = "IA"
            print("\nNIVEL DE DIFICULTAD:")
            print("1. Fácil (movimientos aleatorios)")
            print("2. Difícil (estrategia avanzada)")
            nivel_ia = solicitar_numero("Selecciona el nivel: ", 1, 2)
        
        # ========== VARIABLES DE CONTROL DEL JUEGO ==========
        turno = FICHA_CIRCULO  # El jugador 1 (O) siempre empieza
        partida_activa = True
        
        # ========== BUCLE PRINCIPAL DE LA PARTIDA ==========
        while partida_activa:
            limpiar_pantalla()
            
            # Mostrar información de la partida
            print(f"\n{'=' * 50}")
            print(f"  {nombre_jugador1} (O) vs {nombre_jugador2} (X)")
            print(f"{'=' * 50}")
            
            # Mostrar estado actual del tablero
            mostrar_tablero(tablero)
            
            # Determinar quién es el jugador actual
            nombre_actual = nombre_jugador1 if turno == FICHA_CIRCULO else nombre_jugador2
            simbolo = "O" if turno == FICHA_CIRCULO else "X"
            
            # ========== OBTENER MOVIMIENTO ==========
            if modo_juego == 2 and turno == FICHA_EQUIS:
                # Turno de la IA
                print(f"\n{nombre_actual} está pensando...")
                
                # Seleccionar movimiento según el nivel de dificultad
                if nivel_ia == 1:
                    columna = ia_nivel_1(tablero)
                else:
                    columna = ia_nivel_2(tablero, FICHA_EQUIS, FICHA_CIRCULO, numero_fichas_linea)
                
                # Verificar que la IA pudo hacer un movimiento
                if columna == -1:
                    print("Error: La IA no pudo determinar un movimiento válido.")
                    break
                
                # Pausa para que el usuario vea el pensamiento de la IA
                input("Presiona Enter para ver el movimiento de la IA...")
            else:
                # Turno del jugador humano
                while True:
                    columna = solicitar_numero(
                        f"\n{nombre_actual} ({simbolo}), elige una columna (1-{columnas}): ",
                        1, columnas
                    ) - 1  # Convertir a 0-indexed
                    
                    # Validar que la columna esté disponible
                    if columna_esta_disponible(tablero, columna):
                        break
                    else:
                        print("❌ Columna inválida o llena. Intenta con otra columna.")
            
            # ========== COLOCAR FICHA Y ACTUALIZAR ESTADO ==========
            if colocar_ficha(tablero, turno, columna):
                # Mostrar tablero actualizado con la última ficha resaltada
                limpiar_pantalla()
                print(f"\n{'=' * 50}")
                print(f"  {nombre_jugador1} (O) vs {nombre_jugador2} (X)")
                print(f"{'=' * 50}")
                mostrar_tablero_columna(tablero, columna)
                
                # ========== COMPROBAR CONDICIONES DE FIN ==========
                
                # Comprobar victoria
                if comprobar_linea(tablero, columna, numero_fichas_linea):
                    print(f"\n{'=' * 50}")
                    print(f"  🎉 ¡{nombre_actual} ({simbolo}) HA GANADO! 🎉")
                    print(f"{'=' * 50}")
                    partida_activa = False
                
                # Comprobar empate
                elif not hay_casillas_libres(tablero):
                    print(f"\n{'=' * 50}")
                    print("  🤝 ¡EMPATE! El tablero está lleno.")
                    print(f"{'=' * 50}")
                    partida_activa = False
                
                else:
                    # La partida continúa: cambiar turno
                    turno = FICHA_EQUIS if turno == FICHA_CIRCULO else FICHA_CIRCULO
            else:
                # Error al colocar la ficha (no debería ocurrir con validaciones)
                print("❌ Error al colocar la ficha. Terminando partida.")
                break
        
        # ========== FIN DE LA PARTIDA ==========
        # Preguntar si desea jugar de nuevo
        jugar_de_nuevo = preguntar_jugar_otra_vez()
    
    # Mensaje de despedida
    print("\n¡Gracias por jugar a ConectaN!")
    print("=" * 50)


# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    main()