import evolution


# Ejemplo 1 ---------------------------------------------------
agent_1 = evolution.Agent()
# -------------------------------------------------------------

# Ejemplo 2 ---------------------------------------------------
gen_1 = evolution.Reproduction(value=2,chance_to_mutate=0)
gen_2 = evolution.Diet(value=2, chance_to_go_up=1)
agent_2 = evolution.Agent(genes=[gen_1, gen_2])
# -------------------------------------------------------------

# Ejemplo 3 ---------------------------------------------------
behavior_1 = evolution.Behavior()
agent_3 = evolution.Agent(behavior = behavior_1)
# -------------------------------------------------------------

# Ejemplo 4 ---------------------------------------------------
def diet(agent, element):
    if element.is_agent == True and element.genetic_code.get_code('diet') > 2:
        return True

def diet_move(*args):
    if len(elements) > 2:
        print(2)
    return 0

rule_1 = evolution.EatRule(to_relevance=lambda *args: 0.8)
rule_2 = evolution.Rule('diet', to_see = diet, to_move=diet_move ,to_relevance=lambda *args: 0.5)
behavior_2 = evolution.Behavior(rules=[rule_1, rule_2])
agent_4 = evolution.Agent(genes=[gen_1, gen_2], behavior=behavior_2)
# -------------------------------------------------------------

# Ejemplo 5 ---------------------------------------------------
agent_5 = evolution.Agent(genes=[gen_1], rules=[rule_1, rule_2])
# -------------------------------------------------------------

# Ejemplo 6 ---------------------------------------------------
# Función de filtrado 1
def func(ag: evolution.Agent):
    if (ag.genetic_code.get_gene('speed').value > 5):
        return True
    else:
        return False

# Función de filtrado 2
def func2(ag: evolution.Agent):
    if (ag.genetic_code.get_gene('size').value <= 5):
        return True
    else:
        return False

# Función de filtrado 3
def func3(ag: evolution.Agent):
    if (ag.is_alive):
        return True
    else:
        return False
    
# Función de filtrado 4
def func4(ag: evolution.Agent):
    if (ag.genetic_code.get_gene('reproduction').value == 2
        and ag.genetic_code.get_gene('fertility').value > 4):
        return True
    else:
        return False
# -------------------------------------------------------------

# Ejemplo 7 ---------------------------------------------------
s = evolution.Simulator()
s.create_world(50, 50, 10)

def func_food(simulation):
      return 500-simulation.day

for i in range(5):
    s.add_agent_to_simulation(evolution.Agent())


s.simulate(days = 100,
           food_function=func_food,
           maping=[evolution.MapFunction('speed > 5',func),
                   evolution.MapFunction('size <= 5',func2),
                   evolution.MapFunction('alive',func3),
                   evolution.MapFunction('sexual & fert > 4',func4)],
           plot=1)
# -------------------------------------------------------------

# Ejemplo 8 ---------------------------------------------------
enemies = evolution.EnemiesRule(to_relevance=lambda *args: -1)
visited = evolution.VisitedRule(to_relevance=lambda *args: 1)

behavior_ = evolution.Behavior()
def func_agent():
      return [evolution.Agent() 
              for i in range(50)]
      
sm = evolution.MasterSimulator(trees=10, rounds=30, days=100)
sm.food_distribution = func_food
sm.agents_distribution = func_agent

sm.run(maping=[evolution.MapFunction('alive', func3),
            evolution.MapFunction('size <= 5',func2),
            evolution.MapFunction('speed > 5',func)])
# -------------------------------------------------------------
