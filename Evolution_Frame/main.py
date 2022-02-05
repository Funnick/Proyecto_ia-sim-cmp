import evolution
import agent
import gene
import object_base
import numpy as np
import behavior
from matplotlib import pyplot as plt


def func(ag: agent.Agent):
    if (ag.genetic_code.get_gene('speed').value > 5):
        return True
    else:
        return False


def func2(ag: agent.Agent):
    if (ag.genetic_code.get_gene('size').value <= 5):
        return True
    else:
        return False
  
def func3(ag: agent.Agent):
    if (ag.is_alive):
        return True
    else:
        return False
def func4(ag: agent.Agent):
    if (ag.genetic_code.get_gene('reproduction').value == 2
        and ag.genetic_code.get_gene('fertility').value > 4):
        return True
    else:
        return False

def func5(ag, elem):
    if (isinstance(elem, agent.Agent) and elem.genetic_code.get_gene('diet').value == 2):
        return True
    else:
        return False


def func6(*args):
    print(1)
    return 0

#plt.fill_between([i for i in range(len(agent_cond3))], agent_cond3, alpha=.25)

s = evolution.Simulator()
s.create_world(50, 50)
def func_food(simulation):
      return 700-simulation.day*1

enemies = behavior.EnemiesRule(to_relevance=lambda *args: -1)
visited = behavior.VisitedRule(to_relevance=lambda *args: 1)

behavior_ = behavior.Behavior()
def func_agent():
      return [agent.Agent(behavior=behavior_,genes=[gene.Reproduction(value=2, chance_to_mutate=0)]) for i in range(20)]

for i in range(20):
      s.add_agent_to_simulation(agent.Agent(genes=[gene.Reproduction(value=2, chance_to_mutate=0)]))


s.simulate(100,
           food_function=func_food,
           maping=[evolution.MapFunction('speed > 5',func),
                   evolution.MapFunction('size <= 5',func2),
                   evolution.MapFunction('alive',func3),
                   evolution.MapFunction('sexual & fert > 4',func4)],
           plot=1)
"""
sm = evolution.SimulatorMaster(rounds=30, days=100)
sm.food_distribution = func_food
sm.agents_distribution = func_agent

sm.run(1)
"""

