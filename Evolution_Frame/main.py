import evolution
import agent
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
s.create_world(7, 10)
s.create_agent(3, 10)

s.world.add_food(10)
print(s.world)
print()

s.simulate_one_round()
print(s.world)
