import world, agent


def test_add_agent():
    w = world.World(7, 10)
    r, c = w.get_pos_random_edge()
    a = agent.Agent(r, c, 5, 100)
    w.add_agent(r, c, a)

    assert len(w.map[r][c]) == 2
