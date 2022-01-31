import evolution
import agent
import gene
import object_base
from matplotlib import pyplot as plt

for j in range(30):
      agents = []
      s = evolution.Simulator()
      s.create_world(10, 10, 5)
      #print("Nueva simulacion", j)
      for i in range(5):
            s.add_agent_to_simulation(agent.Agent(-1, -1, 300))
      for i in range(50):
            #print("Nuevo día", i)
            s.world.add_food(100)
            s.simulate_one_round()
            agents.append(s.get_number_of_agents())
      #s.print_footprints(s.world)
      plt.plot([i for i in range(len(agents))], agents, '-', c='r')
plt.show()

#TODO: Agregar los metodos que setean si tiene o no tiene comida arboles etc 
# un tile. 