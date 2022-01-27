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

    def __add__(self, o:Gene):
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
    def __init__(self,
                 value = 15,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
    
    def __str__(self):
        return 'sense'
    
    def mutate(self):
        NotImplemented
    
class Size(Gene):
    def __init__(self,
                 value = 15,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
    
    def __str__(self):
        return 'size'
    
    def mutate(self):
        NotImplemented
    
class Speed(Gene):
    def __init__(self,
                 value = 15,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
        
    def __str__(self):
        return 'speed'
    
    def mutate(self):
        NotImplemented
    
class Reproduction(Gene):
    def __init__(self,
                 value = 0,
                 chance_to_mutate = 0.2,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
    
    def __str__(self):
        return 'reproduction'
    
    def __add__(self, o: Gene):
        return self.value
    
    def mutate(self):
        NotImplemented
    
class Life(Gene):
    def __init__(self,
                 value = 15,
                 chance_to_mutate = 0.5,
                 chance_to_go_up = 0.5):
        Gene.__init__(self, value, chance_to_mutate, chance_to_go_up)
    
    def __str__(self):
        return 'life'
    
    def mutate(self):
        NotImplemented
        
        
class GeneticCode:
    def __init__(self,
                 sense = Sense(),
                 speed = Speed(),
                 size = Size(),
                 reproduction = Reproduction(),
                 life = Life()):
        self.sense = sense
        self.speed = speed
        self.size = size
        self.reproduction = reproduction
        self.life = life
        self.build_chain()
    
    def build_chain(self):
        self.chain = {
            str(self.sense): self.sense,
            str(self.speed): self.speed,
            str(self.size): self.size,
            str(self.reproduction): self.reproduction,
            str(self.life): self.life,
        }
        
    def __add__(self, o: GeneticCode):
        new_chain = {}
        for gene in self.chain.keys():
            new_chain[g] = ((self.chain[g] + o.chain[g])/2)
        return new_chain