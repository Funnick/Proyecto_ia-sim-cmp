import evolution
import agent
import object_base
import gene

s = evolution.Simulator()
"""
s.create_world(7, 10)
s.create_agent(3, 100)
s.world.add_food(10, 5)

print(s.world)
s.simulate_one_agent_action()
print(s.world)
"""
s.create_world(7, 10)
ag = agent.Agent(-1, - 1, 100, gene.Gene(5, 0.5, 0.5))
s.add_agent_to_simulation(ag)

s.world.add_food(10)
print(s.world)
print()

for i in range(10):
    s.simulate_one_round()
    print(s.world)
