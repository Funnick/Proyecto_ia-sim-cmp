import action, world, agent, object_base


def test_move():
    a = agent.Agent(5, 5, 3, 100)
    w = world.World(10, 10)
    w.map[5][5].append(a)
    m = action.Move(4, 5)
    m.execute(w, a)

    assert a.pos_x == 4
    assert a.pos_y == 5
    assert len(w.map[5][5]) == 1
    assert len(w.map[4][5]) == 2


def test_eat():
    a = agent.Agent(5, 5, 3, 100)
    w = world.World(10, 10)
    w.map[5][5].append(a)
    w.map[5][5].append(object_base.Food(5, 5, 100))
    m = action.Eat()
    m.execute(w, a)

    assert w.cell_have_food(5, 5) == False
    assert len(w.map[5][5]) == 2
    assert a.food_eat_today == 1

    a = agent.Agent(5, 5, 3, 100)
    w.map[4][4].append(a)
    m = action.Eat()
    m.execute(w, a)

    assert a.food_eat_today == 0
