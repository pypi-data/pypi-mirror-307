import numpy as np
import matplotlib.pyplot as plt

# Punto es una tupla (x, y)
# Ejemplo: (1, 2)

# Operaciones de puntos, devuelve una nueva tupla
# En vez de hacer clase punto ocupo esto de acá ya que no dejan usar clases y no existen las structs:
# x[0] = x.x
# x[1] = x.y
def suma_puntos(x1, x2):
    return (x1[0] + x2[0], x1[1] + x2[1])

def resta_puntos(x1, x2):
    return (x1[0] - x2[0], x1[1] - x2[1])

# Producto escalar
def escalar(x, k):
    return (x[0] * k, x[1] * k)

# Producto punto
def dot(x1, x2):
    return x1[0] * x2[0] + x1[1] * x2[1]

# Producto cruz
def cross(x1, x2):
    return x1[0] * x2[1] - x1[1] * x2[0]

# Semi plano se define con 1 punto perteneciente a la recta y 1 vector dirección de esta.
# Tupla de dos puntos: (punto perteneciente a la recta, vector dirección)
# Para un semiplano definido por dos puntos P, Q se representa como: (P, Q-P)}
# Los puntos pertecientes al semiplano se encuentran a la izquierda de la recta

# semiplano[0] = punto perteneciente a la recta
# semiplano[1] = dirección de la recta

# Funciones semiplanos

# Devuelve el semiplano correspondiente a la recta que pasa por el segmento
def semiplano(p, q):
    return (p, resta_puntos(q, p))

# Checkea si el punta x está afuera del semiplano
def out(x, semiplano):
    # Explicación matemática: se resta el punto x con el punto del semiplano para obtener un vector que va desde la recta al punto
    # Si ese vector se encuentra a la izquierda del vector de dirección (dentro del semiplano) el producto cruz será postivio o 0
    # el producto cruz será negativo en caso contrario (punto fuera del semiplano)
    return cross(semiplano[1], resta_puntos(x, semiplano[0])) < 0.0

# TODO: borrar esto, setá de más
# Función para comparar semiplanos según el ángulo de su dirección
# def menor_que(s, t):
#     angulo_1 = np.arctan2(s[1][1], s[1][0])
#     angulo_2 = np.arctan2(t[1][1], t[1][0])
#     return angulo_1 < angulo_2

# Devuelve el ángulo del semiplano, esto se ocupa para ordenarlos después
def angulo(s):
    return np.arctan2(s[1][1], s[1][0])

# Punto de interescción de las rectas de dos semiplanos
# Explicación matemática: intersección de dos rectas, la fórmula es:
# Rectas definidas por
# L1 = s0 + alpha s1
# L2 = t0 + beta t2
# Ya y con álgebra y propiedades de productos cruz y volas se iguala L1 y L2, se borra el beta y se llega a una expresión de alpha
# ese alpha es el alpha donde se intersectan, asi que se mete en la formula de L1 y listo,
def interseccion(s, t):
    alpha = cross(resta_puntos(t[0], s[0]), t[1]) / cross(s[1], t[1])
    return suma_puntos(s[0], escalar(s[1], alpha))

# Algoritmo, Recibe una lista de semiplanos

eps = 1e-9 # Epsilon, valor suficientemente pequeño para evaluar si dos floats son iguales
inf = 1e5 # Valor suficientemente grande para tomarlo como infinito, para evitar NaNs

# Ni ahí con explicarlo, cualquier cosa leer el link
def interseccion_semiplanos(semiplanos: list):
    # Se añade una bounding box (cuadrado delimitador muy grande) para el caso de que la intersección de semiplanos quede no acotada
    # Para este problema no debería pasar porque los semiplanos parten de un polígono cerrado pero así está escrito el algoritmo original
    # así que gg no más
    plim1 = (inf, inf)
    plim2 = (-inf, inf)
    plim3 = (-inf, -inf)
    plim4 = (inf, -inf)

    # Añadir los semilpanos de la bounding box a la lista
    semiplanos.append(semiplano(plim1, plim2))
    semiplanos.append(semiplano(plim2, plim3))
    semiplanos.append(semiplano(plim3, plim4))
    semiplanos.append(semiplano(plim4, plim1))

    # Se ordenan los semiplanos
    semiplanos.sort(key=angulo)

    # Inicio algoritmo
    dq = []
    length = 0
    for i in range(len(semiplanos)):
        # Remover los planos del inicio y del final si es que son redundantes
        while length > 1 and out(interseccion(dq[length - 1], dq[length - 2]), semiplanos[i]):
            dq.pop()
            length -= 1

        while length > 1 and out(interseccion(dq[0], dq[1]), semiplanos[i]):
            dq.pop(0)
            length -= 1

        # Caso planos paralelos
        if length > 0 and abs(cross(semiplanos[i][1], dq[length - 1][1])) < eps:
            # Caso planos apuntando en direcciones contraias, intersección vacía
            if dot(semiplanos[i][1], dq[length - 1][1]) < 0:
                return []
            
            # Caso planos apuntando en la misma dirección, se queda el que está más a la izquierda
            if out(dq[length - 1][0], semiplanos[i]):
                dq.pop()
                length -= 1
            else: continue  
        
        # Añadir el nuevo semiplano
        dq.append(semiplanos[i])
        length += 1

    # Último ciclo
    # Checkear los semiplanos del inicio contra los del final
    while length > 2 and out(interseccion(dq[length - 1], dq[length - 2]), dq[0]):
        dq.pop()
        length -= 1

    while length > 2 and out(interseccion(dq[0], dq[1]), dq[length - 1]):
        dq.pop(0)
        length -= 1

    # Caso intersección vacía
    if length < 3: return []

    # Reconstruir el polígono
    puntos_interseccion = []
    for i in range(length - 1):
        puntos_interseccion.append(interseccion(dq[i], dq[i+1]))
    puntos_interseccion.append(interseccion(dq[length - 1], dq[0]))
    return puntos_interseccion

def plot_polygon_kernel(poligono, kernel):
    fig, ax = plt.subplots()
    ax.autoscale()

    # Plot the polygon
    polygon = plt.Polygon(poligono, closed=True, fill=None, edgecolor='b')
    ax.add_patch(polygon)

    # Plot the kernel
    if kernel:
        kernel_polygon = plt.Polygon(kernel, closed=True, color='b', alpha=0.5)
        ax.add_patch(kernel_polygon)

    plt.show()

def plot_star(points):
    semiplanos = []
    for i in range(len(points) - 1):
        semiplanos.append(semiplano(points[i], points[i+1]))
    semiplanos.append(semiplano(points[-1], points[0]))

    kernel = interseccion_semiplanos(semiplanos)

    # Plotear la figura
    plot_polygon_kernel(points, kernel)

def is_star(points):
    semiplanos = []
    for i in range(len(points) - 1):
        semiplanos.append(semiplano(points[i], points[i+1]))
    semiplanos.append(semiplano(points[-1], points[0]))

    kernel = interseccion_semiplanos(semiplanos)
    if kernel:
        return True
    return False