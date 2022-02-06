from random import random, randint

class Gene:
    """
    Clase base de los genes
    """

    def __init__(self,
                 min_level, 
                 max_level, 
                 value, 
                 chance_to_mutate, 
                 chance_to_go_up,
                 step):
        """
        Devuelve un nuevo gen. min_level (1) y max_level (10)
        representan los niveles mínimos y máximos en que puede mutar un gen

        :param min_value: mínimo valor que puede tomar el gen
        :type min_value: int
        :param max_value: máximo valor que puede tomar el gen
        :type max_value: int
        :param value: nivel de la característica
        :type value: int
        :param chance_to_mutate: probabilidad de mutar
        :type chance_to_mutate: float [0, 1]
        :param chance_to_go_up: probabilidad de aumentar en 1 si muta
        :type chance_to_go_up: float [0, 1]
        :param step: tamaño del cambio genético
        :type step: int

        :rtype: Gene
        """
        self.min_level = min_level
        self.max_level = max_level
        self.value = value
        self.chance_to_mutate = chance_to_mutate
        self.chance_to_go_up = chance_to_go_up
        self.step = step

    def __add__(self, o):
        return int((self.value + o.value)/2)

    @property
    def mutate(self):
        """
        Devuelve un gen mutado con probabilidad chance_to_mutate y
        uno idéntico con probabilidad 1 - chance_to_mutate. En caso
        de un gen mutado su valor es +1 con probabilidad chance_to_go_up,
        -1 con el complemento de chance_to_go_up.
        """
        new_value = self.value
        if random() <= self.chance_to_mutate:
            if random() > self.chance_to_go_up and self.value > self.min_level:
                new_value -= self.step
            elif self.value < self.max_level:
                new_value += self.step
        return self.__class__(self.min_level, 
                            self.max_level, 
                            new_value, 
                            self.chance_to_mutate, 
                            self.chance_to_go_up,
                            self.step)
    
    def copy(self):
        """
        Devuelve una copia del gen.
        """
        return self.__class__(self.min_level, 
                            self.max_level, 
                            self.value, 
                            self.chance_to_mutate, 
                            self.chance_to_go_up,
                            self.step)
    
    def def_mutate(self, func):
        """
        Método que agrega una nueva función de mutación.
        """
        self.mutate = func
    
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
                 chance_to_go_up = 0.5,
                 step = 1):
        Gene.__init__(self, 
                      min_level, 
                      max_level, 
                      value, 
                      chance_to_mutate, 
                      chance_to_go_up,
                      step)
    
    def __str__(self):
        return 'sense'
    
class Size(Gene):
    """
    Gen que describe el tamaño del agente.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 10,
                 value = 5,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5,
                 step = 1):
        Gene.__init__(self, 
                      min_level, 
                      max_level, 
                      value, 
                      chance_to_mutate, 
                      chance_to_go_up,
                      step)
    
    def __str__(self):
        return 'size'
      
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
                 chance_to_go_up = 0.5,
                 step = 1):
        Gene.__init__(self, 
                      min_level, 
                      max_level, 
                      value, 
                      chance_to_mutate, 
                      chance_to_go_up,
                      step)
        
    def __str__(self):
        return 'speed'
    
class Reproduction(Gene):
    """
    Gen que describe el tipo de reproducción que
    ejecuta el agente.
    """
    def __init__(self,
                 min_level = 1,
                 max_level =  2,
                 value = 1,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.9,
                 step = 1):
        Gene.__init__(self, 
                      min_level, 
                      max_level, 
                      value, 
                      chance_to_mutate, 
                      chance_to_go_up,
                      step)
    
    def __str__(self):
        return 'reproduction'
    
    def __add__(self, o):
        return self.value
    
    @property
    def mutate(self):
        """
        Mutación de la reproducción, si el agente se encuentra en el
        estado 1 (asexual) y muta, pues hay una alta probabilidad de que
        cambie a estado 2 (sexual). Si se encuentra en el estado 2, hay una muy
        pequeña posibilidad de que cambie al estado 1.
        """
        new_value = self.value
        if random() <= self.chance_to_mutate:
            if self.value == 1 and self.chance_to_go_up < random():
                new_value = 2
            elif self.value == 2 and self.chance_to_go_up > random():
                new_value = 1
        return Reproduction(self.min_level,
                            self.max_level,
                            new_value,
                            self.chance_to_mutate,
                            self.chance_to_go_up,
                            self.step)
        
class Life(Gene):
    """
    Gen que describe la duración de la vida de un
    agente.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 20,
                 value = 10,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5,
                 step = 1):
        Gene.__init__(self, 
                      min_level, 
                      max_level, 
                      value, 
                      chance_to_mutate, 
                      chance_to_go_up,
                      step)
    
    def __str__(self):
        return 'life'
    
class Diet(Gene):
    """
    Gen que describe el tipo de alimentación de un
    agente, o sea, herbívoro, carnívoro u omnívoro.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 3,
                 value = 1,
                 chance_to_mutate = 0.1,
                 chance_to_go_up = 0.8,
                 step = 1):
        
        Gene.__init__(self, 
                      min_level, 
                      max_level, 
                      value, 
                      chance_to_mutate, 
                      chance_to_go_up,
                      step)
    
    def __str__(self):
        return 'diet'
    
    @property
    def mutate(self):
        """
        El tipo de dieta tiene pocas probabilidades de
        cambiar, pero de cambiar, está propenso a ser hacia
        un valor superior.
        """
        new_value = self.value
        if random() <= self.chance_to_mutate:
            if self.value == 1: 
                if self.chance_to_go_up < random():
                    new_value = 3
                else:
                    new_value = 2
            elif self.value == 2:
                if self.chance_to_go_up < random():
                    new_value = 3
                else:
                    new_value = 1
            else:
                if self.chance_to_go_up > random():
                    new_value = randint(1, 2)
        return Diet(self.min_level,
                    self.max_level,
                    new_value,
                    self.chance_to_mutate,
                    self.chance_to_go_up)
    
class Sex(Gene):
    """
    Gen que describe el sexo del agente. Poseerá
    tres estados, 1 si el agente es femenino, 2 si
    es sexual.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 2,
                 value = 1,
                 chance_to_mutate = 1,
                 chance_to_go_up = 0,
                 step = 1):
        value = randint(1, 2)
        Gene.__init__(self, 
                      min_level, 
                      max_level, 
                      value, 
                      chance_to_mutate, 
                      chance_to_go_up,
                      step)
    
    def __str__(self):
        return 'sex'
    
    @property
    def mutate(self):
        """
        Mutación del sexo del agente.
        
        :rtype: Sex
        :return: Sex()
        """
        return Sex()
   
class Fertility(Gene):
    """
    Gen que describe la capacidad del agente engendrar
    uno o más hijos.
    """
    def __init__(self,
                 min_level = 1,
                 max_level = 8,
                 value = 4,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5,
                 step = 1):
        Gene.__init__(self, 
                      min_level, 
                      max_level, 
                      value, 
                      chance_to_mutate, 
                      chance_to_go_up,
                      step)
    
    def __str__(self):
        return 'fertility'
             
class Stamina(Gene):
    """
    Gen que describe la cantidad de energía de un
    agente.
    """
    def __init__(self,
                 min_level = 100,
                 max_level = 1000,
                 value = 400,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5,
                 step = 10):
        Gene.__init__(self, 
                      min_level, 
                      max_level, 
                      value, 
                      chance_to_mutate, 
                      chance_to_go_up,
                      step)
    
    def __str__(self):
        return 'stamina'  
    
    
class Genetic_code:
    """
    Clase dedicada a describir una cadena de genes, o
    código genético.
    """
    def __init__(self, genes = []):
        """
        Se inicializa una cadena genética con un diccionario
        donde irán los genes.
        
        :param genes: genes no predetermidos pasados por el usuario
        :type genes: list[Gene]
        
        :rtype: GeneticCode
        """
        self.build_chain(genes=genes)
              
    def build_chain(self, genes = []):
        """
        Le agrega al código genético los genes preestablecidos.
        
        :param genes: genes no predetermidos pasados por el usuario
        :type genes: list[Gene]
        
        :rtype: None
        """
        
        self.chain = {
            str('sense'): Sense(),
            str('speed'): Speed(),
            str('size'): Size(),
            str('diet'): Diet(),
            str('reproduction'): Reproduction(),
            str('life'): Life(),
            str('sex'): Sex(),
            str('fertility'): Fertility(),
            str('stamina'): Stamina()
        }
        for gene in genes:
            self.add_gene(gene)         
        
    def __add__(self, other):
        """
        Adición de dos cadenas genéticas que devuelve
        una nueva que contiene características de ambas.
        
        :param other: cadena genética de otro agente
        :type other: GeneticCode
        
        :rtype: GeneticCode
        :return: new_genetic_code
        """
        new_genetic_code = Genetic_code()
        new_chain = {}
        for gene in self.chain.keys():
            if random() < 0.5:
                new_chain[gene] = self.chain[gene].copy()
            else:
                new_chain[gene] = other.chain[gene].copy()
            if random() < 0.5:
                new_chain[gene] = new_chain[gene].mutate
        new_genetic_code.chain = new_chain
        return new_genetic_code
    
    def add_gene(self, gene):
        """
        Agrega un gen al código genético
        
        :param gene: gen que será agregado
        :type gene: Gene
        
        :rtype: None
        """
        self.chain[str(gene)] = gene
    
    @property
    def mutate(self):
        """
        Hace mutar todos los genes del código genético
        atendiendo a sus respectivas características.
        
        :rtype: GeneticCode
        :return: new_chain
        """
        new_chain = Genetic_code()
        for gene in self.chain.keys():
            new_chain.chain[gene] = self.chain[gene].mutate
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
