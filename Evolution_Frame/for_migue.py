import evolution
import agent
import gene
import object_base
from matplotlib import pyplot as plt

# Ejemplo crear agente -------------------------------------------------------------------------------

agent.Agent()
agent.Agent(pos_x = -1, pos_y = -1)

g1 = gene.Reproduction(value=2)
g2 = gene.Life(value=10)
agent.Agent(pos_x = -1, pos_y = -1, genes=[g1, g2])

def relevant(agent, element):
    if element:
        return True
    
def function(cell = None, new_cell = None, world = None, path = None, elements = None):
    print(2)
    
def rule(ag):
    if 'pregnant' in self.actual_state:
        return 2
    else:
        return 0

predicate = agent.Predicate('diet', relevant=relevant, function=function, rule=rule)

def state_func(ag):
    if ag.pregnant:
        return True

state = agent.State('pregnant', state_func)
    
agent.Agent(pos_x = -1, pos_y = -1, genes=[g1, g2], behavior=[predicate], states=[state])

# --------------------------------------------------------------------------------------------