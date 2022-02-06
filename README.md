# Evolution Game

## Integrantes

- Miguel Alejandro Rodríguez Hernández
- Manuel  Antonio Vilas Valiente 
- Andrés León Almaguer

[TOC]


## Introducción 

  El objetivo principal del proyecto es simular el comportamiento de diferentes poblaciones de individuos en un entorno abierto donde estos deben de conseguir comida para poder reproducirse, sobrevivir y reproducirse. Al lograr reproducirse estos individuos pueden variar las composición de sus genes, que van desde la forma de reproducción, tipo de alimentación o capacidades que los hacen más aptos para la supervivencia, lo que a su ves puede dar al traste con el cambio de su comportamiento. A lo largo del desarrollo del mismo hemos utilizado el conocimiento aprendido a lo largo del curso en las asignaturas de Simulación, Inteligencia artificial y Compilación.

### Lenguaje y Requerimientos

El lenguaje de programación usado por nosotros en el desarrollo fue [Python](https://www.python.org), elegido sobre todo por el dominio de nosotros los integrantes y por le uso de algunas librerías que permitirían facilitar el desarrollo que en este caso son [matplotlib](https://matplotlib.org) usado para graficar las estadísticas de cada una de las simulaciones y [numpy](https://numpy.org) usada para el calculo con matrices. 

Para el uso del proyecto recomendamos Python 3.9.xx e instalar estas librerías:

```bash
pip install matplotlib numpy
```

## Manual de uso y ejemplos







#### Ejemplo 1

Definir un agente.

```python
agent_1 = agent.Agent()
```

#### Ejemplo 2

Definir nuevos genes y con ellos definir un agente.

```python
gen_1 = gene.Reproduction(value=2,chance_to_mutate=0)
gen_2 = gene.Diet(value=2, chance_to_go_up=1)
agent_2 = agent.Agent(genes=[gen_1, gen_2])
```

#### Ejemplo 3

Establecer un comportamiento a un nuevo agente.

```python
behavior_1 = behavior.Behavior()
agent_3 = agent.Agent(behavior = behavior_1)
```

#### Ejemplo 4

```python
def diet(agent, element):
    if element.is_agent == True and element.genetic_code.get_code('diet') > 2:
        return True

def diet_move(*args):
    if len(elements) > 2:
        print(2)
    return 0

rule_1 = behavior.EatRule(to_relevance=lambda *args: 0.8)
rule_2 = behavior.Rule('diet', to_see = diet, to_move=diet_move ,to_relevance=lambda *args: 0.5)
behavior_2 = behavior.Behavior(rules=[rule_1, rule_2])
agent_4 = agent.Agent(genes=[gen_1, gen_2], behavior=behavior_2)
```



#### Ejemplo 5

Definir un agente a partir de genes y reglas definidas.

```
agent_5 = agent.Agent(genes=[gen_1], rules=[rule_1, rule_2])
```



#### Ejemplo 6

Definición de varias funciones de filtrado de agentes.

```python
# Función de filtrado 1
def func(ag: agent.Agent):
    if (ag.genetic_code.get_gene('speed').value > 5):
        return True
    else:
        return False

# Función de filtrado 2
def func2(ag: agent.Agent):
    if (ag.genetic_code.get_gene('size').value <= 5):
        return True
    else:
        return False

# Función de filtrado 3
def func3(ag: agent.Agent):
    if (ag.is_alive):
        return True
    else:
        return False
    
# Función de filtrado 4
def func4(ag: agent.Agent):
    if (ag.genetic_code.get_gene('reproduction').value == 2
        and ag.genetic_code.get_gene('fertility').value > 4):
        return True
    else:
        return False
```



#### Ejemplo 7

Crear un simulador en un mundo de 50x50.

Define una función de comida.

Agrega 5 agentes y corre dicha simulación por 100 días mapeando los agentes que cumplen las funciones 1 2 3 y 4.

```python
s = evolution.Simulator()
s.create_world(50, 50)

def func_food(simulation):
      return 350-simulation.day

for i in range(5):
    s.add_agent_to_simulation(agent.Agent())


s.simulate(days = 100,
           food_function=func_food,
           maping=[evolution.MapFunction('speed > 5',func),
                   evolution.MapFunction('size <= 5',func2),
                   evolution.MapFunction('alive',func3),
                   evolution.MapFunction('sexual & fert > 4',func4)],
           plot=1)
```



#### Ejemplo 8

[FALTA]

```python
enemies = behavior.EnemiesRule(to_relevance=lambda *args: -1)
visited = behavior.VisitedRule(to_relevance=lambda *args: 1)

behavior_ = behavior.Behavior()
def func_agent():
      return [agent.Agent() 
              for i in range(50)]
      
sm = evolution.Master_simulation(rounds=30, days=100)
sm.food_distribution = func_food
sm.agents_distribution = func_agent
```

#### Ejemplos de los graficos

<img src="./source/Figure_1.png" alt="Ejemplos" style="zoom:70%;" />

<img src="./source/Figure_2.png" alt="Ejemplos" style="zoom:70%;" />

<img src="./source/Figure_3.png" alt="Ejemplos" style="zoom:70%;" />



## La simulación

La simulación tendrá lugar dentro de un mundo bidimensional de casillas donde un conjunto de agentes inteligentes intentaran sobrevivir y reproducirse al competir por comida mientras que en el transcurso de los días, entiéndase día como un ciclo completo de la simulación, los descendientes de estos van a ir variando sus genes o características representativas tratando de acercarse a como funciona la evolución.

### El mapa 

El mundo esta representado por una clase `World` que será el espacio donde ocurrirá la simulación, se encontrarán los agentes y otros objetos esenciales a la simulación, a su vez esta compuesto por un `map` que posee unas dimensiones x e y que determinan el tamaño de esta como el de la simulación en si y esta compuesto por una matriz de `Tile`. En esta clase tenemos un conjunto de métodos que permiten trabajar con los Tiles que nos permiten saber si en un tile determinado existe comida (`Food`), hay un árbol (`Tree`), es un borde, etc. También permite validar si una posible posición es un tile posible para el movimiento, agrega y quita agentes, arboles, comida etc. y chequea la existencia de agentes que puedan realizar la reproducción con otro dado. 

La clase `Tile` es la unidad atómica de espacio en nuestro mundo, el mundo posee un mapa que es una matriz bidimensional de `Tile`. El tile tiene un conjunto de propiedades como son sus coordenadas x e y, si es un borde, si tiene comida (`Food`), agentes (`Agent`) o un árbol (`Tree`) así como un valor entero que determina la altitud del mismo dentro del mundo, una lista objetos (`Object_base`) que se encuentran dentro de la casilla y la lista de feromonas.

La clase `Objetc_base` servirá de molde para las clases que heredaran de ella y tiene como principal y cuenta con sus coordenadas.  De esta tenemos como herederas a `Food` y `Tree`. La primera intuitivamente representa la comida que los agentes que presenten el tipo de alimentación  omnívora y herbívora deben consumir para poder subsistir. Y los Arboles tendrían la particularidad de ser localizaciones alrededor de las cuales tiende a existir un mayor número de comida, aunque poseen un contador y un tiempo de vida máximo. 

### Los agentes 

Los agentes tienen en la simulación un papel protagónico pues podemos decir que la mayoría de las funciones dentro de las misma los tienen a ellos como centro y las interacciones entre estos y el ambiente es el objeto cuasi principal dentro dentro del proyecto, medir la cantidad de agentes dado un conjunto de simulaciones, cual fue su comportamiento y cuales eran las características que los definían nuestras principales variables de estudio.

La clase `Agent` que representa al individuo que interactúa con el ambiente y otros individuos esta definido por su posición en el `map` (x,y) una lista de genes representativas del código genético que van a definir sus características, un `Behavior` que determina el conjunto de reglas (`rules`) que determinarán su comportamiento,  y un `State` en el que estos pueden encontrarse. 

Al definir un nuevo agente serán definidas algunas de sus propiedades como que esta vivo `is_alive` su edad a 0, sus genes a partir de los genes usados como parámetros en el constructor, su energía máxima a partir del gen de *stamina* a partir del cual definimos la energía máxima, la duración de su vida a partir del gen *life*, una función de consumo de energía predefinida. Los `states` pueden ser los definidos en el constructor o en caso de no existir unos definidos por default, y parecido ocurre con el `behavior` que de tener un conjunto de reglas estas serán las cuales definirán el comportamiento del agente o serán aquellas definidas en un `behavior` como parámetro del constructor quedando aquellas no definidas en el constructor las definidas como comportamiento *standard*.

Dentro de los métodos que posee esta clase se encuentran aquellos que tienen que ver con el uso de su código genético, entre los que podremos cambiar genes individuales o el conjunto entero de ellos así como preguntar si el agente posee alguno en especifico. Dentro de estos también tenemos los métodos de reproducción de los individuos en sus variantes sexual o asexual. En el caso de la reproducción sexual el resultado de la unión de dos individuos dará como resultado una lista de agentes que su tamaño dependerá del gen *fertility*, y estos hijos poseerán el comportamiento, `behavior`,  de alguno de los padres además de que su configuración genética será una suma definida en suma de Gene de los códigos de los padres. El caso de la reproducción asexual da como resultado un hijo con el mismo `behavior` que su progenitor y con un código genético alterado o mutado a partir del de su padre.

Otros del los métodos definidos dentro de la clase están aquellos relacionados con el movimiento y los estados de el agente. [Aqui FALTA]

Existe una clase `Action` que determina los cambios ocurridos en el mundo o el agente, de estas heredan un conjunto de otras acciones como son `DoNothing`, `MoveNorth`, `MoveSouth`, `MoveEast`, `MoveWest`, `Eat` y `HaveSex` que son bastante explicativas en sus nombres y tienen que ver como se intuye con el movimiento alimentación y reproducción respectivamente en los individuos.

La clase `Footprint` se usa para representar las pisadas dejadas por un agente al trasladarse por una casilla usada para ayudar a las agentes a tener un método de orientación dentro del terreno. [^ 1]

### Los genes 

Como explicamos previamente, el código genético de cada individuo determina su comportamiento por lo que repercute de forma directa o indirecta en su comportamiento al incidir en las reglas que definen su `behavior`. Con el objetivo de poder variar parámetros dentro de las características de los individuos surge esta clase `Gene`, que va a representar cada una de estas características representativas del agente y la clase `Genetic_code` que representa al conjunto de los `Gene` que posee un `Agent` .

Cada Gene está definido por los valores mínimo y máximo que puede alcanzar de tipo enteros, el valor actual que posee, probabilidades de mutar y aumentar del tipo *float* y el tamaño del cambio que pueden llegar a realizar. La suma o unión de dos genes esta definida por default como el truncamiento a entero de la media de los valores de los genes. Al mutar un gene se devuelve un gen mutado con += el step que este posee en dependencia de una propiedad aleatoria sobrepase los umbrales de probabilidad de mutar y de aumentar, si solo muta decrecerá su valor y si muta y aumenta lo contrario. Además de poseer la posibilidad de implementar nuevas funciones de mutación para los mismos.

Dentro de los genes definidos para la simulación se encuentran:

- Sense:  Define la capacidad del agente de percibir el medio que le rodea.
- Size: Define su tamaño.
- Speed:  Velocidad del agente lo que determina la cantidad de casillas que puede desplazarse por ronda.
- Reproduction: Tipo de reproducción que posee el agente, sexual o asexual.
- Life: Duración de la vida del agente.
- Diet: Tipo de comida que consume, puede ser herbívoro, carnívoro u omnívoro.
- Sex: Sexo del agente, posee tres estados asexual, sexual femenino y sexual masculino.
- Fertility: Capacidad del agente de poseer un mayor número de descendientes.
- Stamina: Cantidad de energía del agente necesaria para desplazarse.



#### Tabla de valores por default de los genes 

|     Gen      | min_value | max_value | value | ch_to_mutate | ch_to_go_up | step |
| :----------: | :-------: | :-------: | :---: | :----------: | :---------: | :--: |
|    Sense     |     1     |    10     |   5   |     0.5      |     0.5     |  1   |
|     Size     |     1     |    10     |   5   |     0.5      |     0.5     |  1   |
|    Speed     |     1     |    10     |   5   |     0.5      |     0.5     |  1   |
| Reproduction |     1     |     2     |   1   |     0.5      |     0.9     |  1   |
|     Life     |     1     |    20     |  10   |     0.5      |     0.5     |  1   |
|     Diet     |     1     |     3     |   1   |     0.1      |     0.8     |  1   |
|     Sex      |     1     |     2     |   1   |      1       |      0      |  1   |
|  Fertility   |     1     |     8     |   4   |     0.5      |     0.5     |  1   |
|   Stamina    |    100    |   1000    |  400  |     0.5      |     0.5     |  10  |

  En los casos de *Sense*, *Size*, *Speed*, *Life*, *Fertility* y *Stamina* su capacidad de mutar estará definida por el modo estándar  explicado anteriormente. Pero en los casos de *Reproduction*, *Diet* y *Sex* tendrán sus propios métodos de mutación. La mutación en la *Reproduction* solo posee dos valores que representan el 1 del tipo asexual y el 2 del tipo sexual y las probabilidades de pasar de 1 a 2 (9/10) son mucho mayores que de 2 a 1 (1/9). El caso de *Diet* esta compuesta por una terna 1 herbívoros, 2 carnívoros y 3 omnívoros, al poseer altas posibilidades de mutar hacia arriba es tenderán a mutar hacia omnívoros dado que si están en estado 1 y mutan tendrán una probabilidad del 4/5 de pasar al estado 3, ocurre lo mismo de con 2 con mayor tendencia hacia estado 3 y en el caso de poseer alimentación omnívora tendrá igual oportunidad de pasar a 1 o 2. El *Sex* tiene tres estados 1 asexual, 2 sexual femenino ♀ y 3 sexual masculino ♂. 

El `Genetic_code` esta compuesto por un diccionario de nombre del gen a `Gene` y será definido por una lista de genes no predeterminados definidos por el usuario que serán combinados con los estándares. Además de poseer la posibilidad de unir dos cadenas, mutar todos los genes de una cadena, preguntar por la existencia del algún `Gene` .

### El comportamiento

[FALTA]

### El simulador

El simulador es la clase que controla los procesos internos de la simulación, la pone a funcionar es la que posee al mundo y dentro de este, los agentes. Esta definida por un `world`, un conjunto de restricciones, los agentes el ciclo o día actual de la simulación y una función de comida. Entre las prestaciones con las que cuenta además de las de iniciar nuevos mundos definir una función de comida que nos permite determinar cuanta comida queremos que se genere dentro del tablero según que ciclo,  la posibilidad de agregar ciertas restricciones a la simulación para hacerla mas restrictiva, adicionar agentes, eliminarlos etc. 

Cada simulación esta dividida en días o ciclos, por cada día se pasa a ubicar la comida en los `Tiles` a partir de la función si esta existe, se simula una ronda donde cada uno de los agentes ejecuta una `Action`, se eliminan de esta aquellos que no pudieron llegar a conseguir comida, se reproducen aquellos que cumplan las condiciones para ello y se resetean sus estados para la próxima ronda así hasta que se llega al final de los días seleccionados por el usuario. Las estadísticas de cada unas de estas rondas son recogidas para luego ser mostradas. 

[FALTA]

[aqui pon el Master simulation que tuve que cambiarle el nombre pq no sabia si era el maestro simulador Simulator Master como tu lo tenias o Master simulation como lo traduje yo de tu docstring]   





[^ 1]: Ver esto luego