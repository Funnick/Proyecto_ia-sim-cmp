from random import random


class Gene:
    """
    Clase base de los genes
    """

    def __init__(self, value, chance_to_mutate, chance_to_go_up):
        """
        Devuelve un nuevo gen. min_level (1) y max_level (10)
        representan los niveles mínimos y máximos en que puede mutar un gen

        :param value: nivel de la característica
        :type value: int
        :param chance_to_mutate: probabilidad de mutar
        :type chance_to_mutate: float [0, 1]
        :param chance_to_go_up: probabilidad de aumentar en 1 si muta
        :type chance_to_go_up: float [0, 1]

        :rtype: Gene
        """
        self.min_level = 1
        self.max_level = 10
        self.value = value
        self.chance_to_mutate = chance_to_mutate
        self.chance_to_go_up = chance_to_go_up

    def __add__(self, o):
        return (self.value + o.value)/2

    def mutate(self):
        """
        Devuelve un gen mutado con probabilidad chance_to_mutate y
        uno idéntico con probabilidad 1 - chance_to_mutate. En caso
        de un gen mutado su valor es +1 con probabilidad chance_to_go_up,
        -1 con el complemento de chance_to_go_up.
        """
        if random() <= self.chance_to_mutate:
            if random() > self.chance_to_go_up and self.value > self.min_level:
                return Gene(self.value - 1, self.chance_to_mutate, self.chance_to_go_up)
            elif self.value < self.max_level:
                return Gene(self.value + 1, self.chance_to_mutate, self.chance_to_go_up)
        return Gene(self.value, self.chance_to_mutate, self.chance_to_go_up)
    
class Sense(Gene):
    """
    Gen que describe la capacidad del agente para
    percibir el medio que le rodea.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 10,
                 value = 5,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
    
    def __str__(self):
        return 'sense'
    
    #def mutate(self):
    #    NotImplemented
    
class Size(Gene):
    """
    Gen que describe el tamaño del agente.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 10,
                 value = 5,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
    
    def __str__(self):
        return 'size'
    
    #def mutate(self):
    #    NotImplemented
    
class Speed(Gene):
    """
    Gen que describe la velocidad con la que se
    desplaza el agente.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 10,
                 value = 5,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
        
    def __str__(self):
        return 'speed'
    
    #def mutate(self):
    #    NotImplemented
    
class Reproduction(Gene):
    """
    Gen que describe el tipo de reproducción que
    ejecuta el agente.
    """
    def __init__(self,
                 min_level = 1,
                 max_level =  2,
                 value = 1,
                 chance_to_mutate = 0.01,
                 chance_to_go_up = 0.9):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
    
    def __str__(self):
        return 'reproduction'
    
    def __add__(self, o):
        return self.value
    
    def mutate(self):
        """
        Mutación de la reproducción, si el agente se encuentra en el
        estado 1 (asexual) y muta, pues hay una alta probabilidad de que
        cambie a estado 2 (sexual). Si se encuentra en el estado 2, hay una muy
        pequeña posibilidad de que cambie al estado 1.
        """
        if random() <= self.chance_to_mutate:
            if self.value == 1 and self.chance_to_go_up < random():
                self.value == 2
            elif self.value == 2 and self.chance_to_go_up > random():
                self.value = 1
class Life(Gene):
    """
    Gen que describe la duración de la vida de un
    agente.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 10,
                 value = 5,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
    
    def __str__(self):
        return 'life'
    
    #def mutate(self):
    #    NotImplemented
    
class Diet(Gene):
    """
    Gen que describe el tipo de alimentación de un
    agente, o sea, hervívoro, carnívoro o omnívoro.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 10,
                 value = 5,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
    
    def __str__(self):
        return 'diet'
    
    #def mutate(self):
    #    NotImplemented
        
class GeneticCode:
    """
    Clase dedicada a describir una cadena de genes, o
    código genético.
    """
    def __init__(self,
                 sense = Sense(),
                 speed = Speed(),
                 size = Size(),
                 diet = Diet(),
                 reproduction = Reproduction(),
                 life = Life()):
        """
        Se inicializa una cadena genética con los genes
        preestablecidos.
        
        :param sense: gen de la visión  dentro de la cadena
        :type sense: Sense
        :param speed: gen de la velocidad dentro de la cadena
        :type speed: Speed
        :param size: gen del tamaño dentro de la cadena
        :type size: Size
        :param diet: gen del tipo de dieta dentro de la cadena
        :type diet: Diet 
        :param reproduction: gen del tipo de reproducción dentro de la cadena
        :type reproduction: Reproduction
        :param life: gen de la espezanza de vida dentro de la cadena
        :type life: Life
        """
        self.sense = sense
        self.speed = speed
        self.size = size
        self.diet = diet
        self.reproduction = reproduction
        self.life = life
        self.build_chain()
    
    def build_chain(self):
        self.chain = {
            str(self.sense): self.sense,
            str(self.speed): self.speed,
            str(self.size): self.size,
            str(self.diet): self.diet,
            str(self.reproduction): self.reproduction,
            str(self.life): self.life,
        }
        
    def __add__(self, other):
        """
        Adición de dos cadenas genéticas que devuelve
        una nueva que contiene características de ambas.
        
        :param other: cadena genética de otro agente
        :type other: GeneticCode
        
        :rtype: GeneticCode
        :return: new_chain
        """
        new_chain = {}
        for gene in self.chain.keys():
            if random() < 0.5:
                new_chain[g] = self.chain[g]
            else:
                new_chain[g] = other.chain[g]
        return new_chain
    
    def add_gene(self, gene):
        """
        Agrega un gen al código genético
        
        :param gene: gen que será agregado
        :type gene: Gene
        
        :rtype: None
        """
        self.chain[str(gene)] = gene
    
    def code(self):
        """
        Retorna el diccionario que describe el código
        genético.
        
        :rtype: dict
        :return: self.chain
        """
        return self.chain
    
    def mutate(self):
        """
        Hace mutar todos los genes del código genético
        atendiendo a sus respectivas características.
        
        :rtype: GeneticCode
        :return: new_chain
        """
        new_chain = GeneticCode()
        for gene in self.chain.keys():
            new_chain.chain[gene] = self.chain[gene].mutate()
        return new_chain
    
    def get_gene(self, gene):
        """
        Devuelve un gen de la cadena genética.
        
        :rtype: Gene
        :return: self.chain[gene]
        """
        return self.chain[gene]
    
    def have_gene(self, gene):
        """
        Devuelve verdadero o falso en dependencia de
        si existe o no un gen en el código genético.
        
        :rtype: bool
        :return: True | False
        """
        return str(gene) in self.code().keys()