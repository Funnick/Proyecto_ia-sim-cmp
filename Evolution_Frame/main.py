import evolution
import agent
import gene
import object_base
from matplotlib import pyplot as plt

for j in range(30):
      agents = []
      s = evolution.Simulator()
      s.create_world(30, 30, 5)
      print("Nueva simulacion", j)
      for i in range(5):
            s.add_agent_to_simulation(agent.Agent(-1, -1, 200))
      for i in range(100):
            #print("Nuevo día", i)
            s.world.add_food(50)
            s.simulate_one_round()
            agents.append(s.get_number_of_agents())
      #s.print_footprints(s.world)
      plt.plot([i for i in range(len(agents))], agents, '-')
plt.show()

#TODO: Agregar los metodos que setean si tiene o no tiene comida arboles etc 
# un tile. 