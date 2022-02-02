class Bayes(object):
    def __init__(self):
        self._container = dict()
    def Set(self,hypothis,prob):
        self._container[hypothis]=prob
    def Mult(self,hypothis,prob):
        old_prob = self._container[hypothis]
        self._container[hypothis] = old_prob*prob
    def Normalize(self):
        count = 0
        for hypothis in self._container.values():
            count=count+hypothis
        for hypothis,prob in self._container.items():
            self._container[hypothis]=self._container[hypothis]/count
    def Prob(self,hypothis):
        Prob = self._container[hypothis]
        return Prob
    
#Instanta la clase Bayes
bayes = Bayes()
 
 # Probabilidad a priori
bayes.Set ('Bow_A', 0.5) #P (  A) = 1/2
bayes.Set ('Bow_B', 0.5) #P (  B) = 1/2

#Probabilidad posterior 
bayes.Mult('Bow_A', 0.75)
bayes.Mult('Bow_B', 0.5)
 
bayes.Normalize()
prob = bayes.Prob ('Bow_A') # P (Tazón A | Pastel de vainilla)
print ('Probabilidad de galletas de vainilla del canal del tazón A: {}'.format(prob))