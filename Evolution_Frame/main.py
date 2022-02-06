import evolution
import agent
import gene
import object_base
import behavior
from matplotlib import pyplot as plt
import aux_meth


# Ejemplo 1 ---------------------------------------------------
agent_1 = agent.Agent()
# -------------------------------------------------------------

# Ejemplo 2 ---------------------------------------------------
gen_1 = gene.Reproduction(value=2,chance_to_mutate=0)
gen_2 = gene.Diet(value=2, chance_to_go_up=1)
agent_2 = agent.Agent(genes=[gen_1, gen_2])
# -------------------------------------------------------------

# Ejemplo 3 ---------------------------------------------------
behavior_1 = behavior.Behavior()
agent_3 = agent.Agent(behavior = behavior_1)
# -------------------------------------------------------------

# Ejemplo 4 ---------------------------------------------------
def diet(agent, element):
    if element.is_agent == True and element.genetic_code.get_code('diet') > 2:
        return True

def diet_move(*args):
    if len(elements) > 2:
        print(2)
    return 0

rule_1 = behavior.EatRule(to_relevance=lambda *args: 0.8)
rule_2 = behavior.Rule('diet', to_see = diet, to_move=diet_move ,to_relevance=lambda *args: 0.5)
behavior_2 = behavior.Behavior(rules=[rule_1, rule_2])
agent_4 = agent.Agent(genes=[gen_1, gen_2], behavior=behavior_2)
# -------------------------------------------------------------

# Ejemplo 5 ---------------------------------------------------
agent_5 = agent.Agent(genes=[gen_1], rules=[rule_1, rule_2])
# -------------------------------------------------------------

# Ejemplo 6 ---------------------------------------------------
# Función de filtrado 1
def func(ag: agent.Agent):
    if (ag.genetic_code.get_gene('speed').value > 5):
        return True
    else:
        return False

# Función de filtrado 2
def func2(ag: agent.Agent):
    if (ag.genetic_code.get_gene('size').value <= 5):
        return True
    else:
        return False

# Función de filtrado 3
def func3(ag: agent.Agent):
    if (ag.is_alive):
        return True
    else:
        return False
    
# Función de filtrado 4
def func4(ag: agent.Agent):
    if (ag.genetic_code.get_gene('reproduction').value == 2
        and ag.genetic_code.get_gene('fertility').value > 4):
        return True
    else:
        return False
# -------------------------------------------------------------

# Ejemplo 7 ---------------------------------------------------
s = evolution.Simulator()
s.create_world(50, 50)

def func_food(simulation):
      return 350-simulation.day

for i in range(5):
    s.add_agent_to_simulation(agent.Agent())


s.simulate(days = 100,
           food_function=func_food,
           maping=[evolution.MapFunction('speed > 5',func),
                   evolution.MapFunction('size <= 5',func2),
                   evolution.MapFunction('alive',func3),
                   evolution.MapFunction('sexual & fert > 4',func4)],
           plot=1)
# -------------------------------------------------------------

# Ejemplo 8 ---------------------------------------------------
enemies = behavior.EnemiesRule(to_relevance=lambda *args: -1)
visited = behavior.VisitedRule(to_relevance=lambda *args: 1)

behavior_ = behavior.Behavior()
def func_agent():
      return [agent.Agent() 
              for i in range(50)]
      
sm = evolution.Master_simulation(rounds=30, days=100)
sm.food_distribution = func_food
sm.agents_distribution = func_agent

"""sm.run(plot = 1, maping=[aux_meth.MapFunction('alive', func3),
                         aux_meth.MapFunction('size <= 5',func2),
                         aux_meth.MapFunction('speed > 5',func)])"""
# -------------------------------------------------------------
