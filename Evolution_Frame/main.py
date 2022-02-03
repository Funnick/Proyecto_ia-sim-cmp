# from Evolution_Frame.agent import Agent
import evolution
import agent
import gene
import object_base
from matplotlib import pyplot as plt

def start_simulations ():
      print("Bienvenido al simulador \n diga cuantos simulaciones desea hacer:")
      sims = int(input())
      for j in range(sims):
            print("filas, columnas, dias, arboles, agentes, comida")
            x = input().split()
            y = []
            for i in x: 
                  y.append(int(i))
            agents = run_simulation(y[0],y[1],y[2],y[3],y[4],y[5])
            plt.plot([i for i in range(len(agents))], agents, '-')
      plt.show()

def run_simulation(world_x:int,world_y:int,days:int,trees:int,agents_amount:int,food_indx:int):
      no_agents = []
      sim = evolution.Simulator()
      sim.create_world(world_x,world_y,trees)
      for a in range(agents_amount):
            sim.add_agent_to_simulation(agent.Agent(-1,-1,200))
      for d in range(days):
            sim.world.add_food(food_indx)
            sim.simulate_one_round()
            no_agents.append(sim.get_number_of_agents())
      print("fin de la simulacion")
      return no_agents

# def run_simulation(world_x:int,world_y:int,days:int,trees:int,agents:list,food_indx:int):
#       no_agents = []
#       sim = evolution.Simulator()
#       sim.create_world(world_x,world_y,trees)
#       for a in agents:
#             sim.add_agent_to_simulation(a)
#       for d in range(days):
#             sim.world.add_food(food_indx)
#             sim.simulate_one_round()
#             no_agents.append(sim.get_number_of_agents())
#       print("fin de la simulacion")
#       return no_agents

# def run_simulation(world_x:int,world_y:int,days:int,trees:int,agents_amount:int,food_function):
#       no_agents = []
#       sim = evolution.Simulator()
#       sim.create_world(world_x,world_y,trees)
#       for a in range(agents_amount):
#             sim.add_agent_to_simulation(agent.Agent(-1,-1,200))
#       for d in range(days):
#             sim.world.add_food(food_function[d])
#             sim.simulate_one_round()
#             no_agents.append(sim.get_number_of_agents())
#       print("fin de la simulacion")
#       return no_agents

# def run_simulation(world_x:int,world_y:int,days:int,trees:int,agents:list,food_function):
#       no_agents = []
#       sim = evolution.Simulator()
#       sim.create_world(world_x,world_y,trees)
#       for a in agents:
#             sim.add_agent_to_simulation(a)
#       for d in range(days):
#             sim.world.add_food(food_function[d])
#             sim.simulate_one_round()
#             no_agents.append(sim.get_number_of_agents())
#       print("fin de la simulacion")
#       return no_agents

# for j in range(30):
#       agents = []
#       s = evolution.Simulator()
#       s.create_world(30, 30, 5)
#       print("Nueva simulacion", j)
#       for i in range(5):
#             s.add_agent_to_simulation(agent.Agent(-1, -1, 200))
#       for i in range(100):
#             #print("Nuevo día", i)
#             s.world.add_food(50)
#             s.simulate_one_round()
#             agents.append(s.get_number_of_agents())
#       #s.print_footprints(s.world)
#       plt.plot([i for i in range(len(agents))], agents, '-')
# plt.show()

#TODO: Agregar los metodos que setean si tiene o no tiene comida arboles etc 
# un tile. 

class Function():
      def __init__ (self,x:dict):
            self.dic_xy = x
            pass
            
      def __init__ (self,y:list):
            i = 0
            self.dic_xy = {}
            for value in y:
                  self.dic_xy[i] = value
                  i +=1

      def __init__ (self,x:list,y:list):
            self.dic_xy = {}
            x_index = 0
            for i in range (x[-1]+1):
                  self.dic_xy[i] = y[x_index]
                  if i == x[x_index]:
                        x_index = x_index+1

      def __getitem__ (self,x):
            return self.dic_xy[x]

      def __len__(self):
            return len(self.dic_xy)


# f = Function([3,7,10],[1,2,3])
# print(f[5])
start_simulations()