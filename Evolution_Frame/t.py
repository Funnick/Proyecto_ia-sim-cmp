import object_base
import world
import agent
import action
import random


o = object_base.ObjectBase(0, 0)

print(o)
print(o.pos_x, o.pos_y, o.is_edge)

print()

e = object_base.Edge(2, 2)
print(e)
print(e.pos_x, e.pos_y, e.is_edge)

print()

f = object_base.Food(1, 2, 50)
print(f)
print(f.pos_x, f.pos_y, f.stored_energy, f.is_edge)

print()

w = world.World(10, 7)
print(w)
w.add_food(5, 50)
print(w)

print()

a = agent.Agent(5, 3, 2, 100)
print(a)
w.map[5][3].append(a)
print(a.see(w))
print()
# print((0,0) + (1, 3))
print()
print(a.go_to_edge(a.see(w)))
print()
print()
print(a.play(a.see(w)))
print(a.get_random_move(a.see(w)))
print(a.look_for_food(a.see(w)))
mn = action.MoveNorth()
mn.execute(w, a)
print(w)
