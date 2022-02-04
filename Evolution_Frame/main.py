import evolution
import agent
import gene
import object_base
from matplotlib import pyplot as plt
import numpy as np

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
def func3(ag, elem):
      if (isinstance(elem, agent.Agent) and elem.genetic_code.get_gene('diet').value > 1):
            return True
      else:
            return False

def func4(*args):
      print(1)
      return 0

for j in range(30):
      agents = []
      s = evolution.Simulator()
      s.create_world(50, 50)
      print("Nueva simulacion", j)
      for i in range(5):
            ag = agent.Agent(-1, -1)
            pred = agent.Predicate('diet', relevant=func3, function=func4, rule=lambda agent:1)
            #ag.behavior.set_predicate(pred)
            s.add_agent_to_simulation(ag)
      for i in range(100):
            #print("Nuevo día", i)
            s.world.add_food(500 - i*5)
            s.simulate_one_round()
            agents.append(s.get_number_of_agents())
      #s.print_footprints(s.world)
      plt.plot([i for i in range(len(agents))], agents, '-', alpha = 0)
      plt.fill_between([i for i in range(len(agents))], agents, alpha=.25)
plt.show()
#TODO: Agregar los metodos que setean si tiene o no tiene comida arboles etc 
# un tile.
"""

agents = []
agent_cond = []
agent_cond2 = []
agent_cond3 = []
s = evolution.Simulator() 
s.create_world(100, 100, 100)
for i in range(20):
      s.add_agent_to_simulation(agent.Agent(-1, -1, [gene.Stamina(value=500)]))
for i in range(365):
      s.world.add_food(1000-i*2)
      agent_cond.append(len(s.get_agents_that(func)))
      agent_cond2.append(len(s.get_agents_that(func2)))
      agent_cond3.append(len(s.get_agents_that(func3)))
      agents.append(s.get_number_of_agents())
      s.simulate_one_round()
#s.print_footprints(s.world)
plt.plot([i for i in range(len(agents))], agents, '-', alpha=1.00)
plt.fill_between([i for i in range(len(agents))], agents, alpha=.25)

plt.plot([i for i in range(len(agent_cond))], agent_cond, '-', alpha=1.00)
plt.fill_between([i for i in range(len(agent_cond))], agent_cond, alpha=.25)
plt.plot([i for i in range(len(agent_cond2))], agent_cond2, '-', alpha=1.00)
plt.fill_between([i for i in range(len(agent_cond2))], agent_cond2, alpha=.25)
plt.plot([i for i in range(len(agent_cond3))], agent_cond3, '-', alpha=1.00)
plt.fill_between([i for i in range(len(agent_cond3))], agent_cond3, alpha=.25)
plt.show()
"""
"""
s = evolution.Simulator() 
s.create_world(10, 10, 5)
s.add_agent_to_simulation(agent.Agent(-1, -1, 200))
for i in range(30):
      #print("Nuevo día", i)
      s.world.add_food(10)
      s.simulate_one_round()
      #s.print_footprints(s.world)
      
"""