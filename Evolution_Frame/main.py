import evolution
import agent
import gene
import object_base
import numpy as np
from matplotlib import pyplot as plt


def func(ag: agent.Agent):
    if (ag.genetic_code.get_gene('sense').value > 5):
        return True
    else:
        return False


def func2(ag: agent.Agent):
    if (ag.genetic_code.get_gene('size').value > 5):
        return True
    else:
        return False
  
def func3(ag: agent.Agent):
    if (ag.genetic_code.get_gene('size').value <= 5):
        return True
    else:
        return False
def func4(ag: agent.Agent):
    if (ag.genetic_code.get_gene('diet').value >1):
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
      return 500

def func_agent():
      return [agent.Agent() for i in range(10)]

for i in range(5):
      ag = agent.Agent()
      ag.behavior.rules['enemies'].to_relevance = lambda *args: -0.5
      s.add_agent_to_simulation(agent.Agent())


s.simulate(365,
           food_function=func_food,
           maping=[evolution.MapFunction('see > 5',func),
                   evolution.MapFunction('size > 5',func2),
                   evolution.MapFunction('size <= 5',func3),
                   evolution.MapFunction('diet > 1',func4)],
           plot=1)

sm = evolution.SimulatorMaster(rounds=30)
sm.food_distribution = func_food
sm.agents_distribution = func_agent

sm.run(1)


