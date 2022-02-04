import numpy as np

def generate_perlin_noise_2d(shape, res):
    """
    Algoritmo de Perlin Noise.
    
    :param shape: tupla de dimensiones de la matriz a crear.
    :type shape: tuple(int, int)
    :param res: tupla de valores más pequeños que dividen a las dimensiones.
    :type shape: tuple(int, int)
    
    :rtype: np.array
    :return: np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)
    """
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    
    # Gradientes
    angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:,1:].repeat(d[0], 0).repeat(d[1], 1)
    
    # Rampas
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1]-1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
    
    # Interpolación
    t = f(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
    return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)

def generate_elevation_matrix(dimension_x, dimension_y):
    """
    Genera una matriz de elevación, con valores entre -10 y 10
    con el uso del algoritmo Perlin Noise.
    
    :param dimension_x: cantidad de filas de la matriz
    :type dimension_x: int
    :param dimension_y: cantidad de columnas de la matriz
    :type dimension_y: int
    
    :rtype: list
    :return: elevation
    """
    shape_x = 2 if dimension_x % 2 == 0 else 0
    shape_y = 2 if dimension_y % 2 == 0 else 0
    b = 3
    while 1:
        if shape_x and shape_y:
            break
        if not shape_x and not dimension_x % b:
            shape_x = b
        if not shape_y and not dimension_y % b:
            shape_y = b
        b+=2
    a = generate_perlin_noise_2d((dimension_x,dimension_y),(shape_x,shape_y))
    elevation=[]
    for i in range(dimension_x):
        elevation.append([])
        for j in range(dimension_y):
            elevation[i].append(round(a[i][j]*10))
               
    return elevation      

def mean(array):
    """
    Función para calcular la media, dando relevancia a los
    valores más pequeños.
    
    :param array: lista de elementos a hallarle la media
    :type array: list
    
    :rtype: float
    :return: mean
    """
    total = len(array)
    sum_elem = 0
    for elem in array:
        sum_elem = sum_elem + 1/elem if elem != 0 else sum_elem + 1
    mean = total/sum_elem if len(array) or sum_elem!=0 else 0
    return mean

def manhattan(pos1, pos2):
    """
    Función para calcular la distancia manhattan entre
    dos coordenas de una matriz
    
    :param pos1: primera coordenada
    :type pos1: Tuple[int, int]
    :param pos2: segunda coordenada
    :type pos2: Tuple[int, int]
    
    :rtype: int
    :return: distance
    """
    distance = int(abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))
    return distance