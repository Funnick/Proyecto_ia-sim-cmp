import evolution
import agent
import gene
import object_base

s = evolution.Simulator()
"""
s.create_world(7, 10)
s.create_agent(3, 100)
s.world.add_food(10, 5)

print(s.world)
s.simulate_one_agent_action()
print(s.world)
"""
s.create_world(dimension_x= 5,dimension_y= 10, trees = 3)
a = agent.Agent(-1, -1, 100)
a1 = agent.Agent(-1, -1, 100)
a2 = agent.Agent(-1, -1, 100)
a3 = agent.Agent(-1, -1, 100)
a4 = agent.Agent(-1, -1, 100)
s.add_agent_to_simulation(a)
s.add_agent_to_simulation(a1)
s.add_agent_to_simulation(a2)
s.add_agent_to_simulation(a3)
#s.add_agent_to_simulation(a4)
def f(s):
      if s.get_days() > 10:
            return False
      
for i in range(10):
      print(s.world)
      s.world.add_food(8)
      print('-----------------------------')
      print(s.world)
      s.simulate_one_round()
      print(s.world)
      print('-----------------------------')    