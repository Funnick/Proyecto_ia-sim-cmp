from typing import Any
from .utils import ReturnException
from evolution import agent, evolution


def p(context, args):
    print(args[0].execute(context))


def create_simulator(context, args):
    return evolution.Simulator()


def get_simulation_day(context, args):
    s = args[0].execute(context)
    return s.day


def get_simulation_agents_count(context, args):
    s = args[0].execute(context)
    return len(s.agents)


def create_agent(context, args):
    return agent.Agent()


def add_agent_to_simulation(context, args):
    s = args[0].execute(context)
    s.add_agent_to_simulation(args[1].execute(context))


def simulate(context, args):
    s = args[0].execute(context)
    s.simulate()


def create_world(context, args):
    s = args[0].execute(context)
    s.create_world(
        args[1].execute(context), args[2].execute(context), args[3].execute(context)
    )


def get_agent_attr_gene(context, args):
    ag = args[0].execute(context)
    gene = args[1].execute(context)
    attr = args[2].execute(context)
    return ag.genetic_code.get_gene(gene).get_attr(attr)


def set_agent_attr_gene_value(context, args):
    ag = args[0].execute(context)
    gene = args[1].execute(context)
    attr = args[2].execute(context)
    value = args[3].execute(context)
    return ag.genetic_code.get_gene(gene).set_attr_value(attr, value)


def get_agent_value_gene(context, args):
    ag = args[0].execute(context)
    gene = args[1].execute(context)
    return ag.genetic_code.get_gene(gene).value


def set_agent_value_gene(context, args):
    ag = args[0].execute(context)
    gene = args[1].execute(context)
    ag.genetic_code.get_gene(gene).value = args[2].execute(context)


def create_list(context, args):
    return []


def add_elem_to_list(context, args):
    l = args[0].execute(context)
    e = args[1].execute(context)
    l.append(e)


def remove_pos_from_list(context, args):
    l = args[0].execute(context)
    p = args[1].execute(context)
    l.pop(p)


class AgentPredicate:
    def __init__(self, context, predicate) -> None:
        self.context = context
        self.predicate = predicate

    def __call__(self, agent, *args: Any, **kwds: Any) -> Any:
        c = self.context.get_child()
        c.define_var(self.predicate.param_list[0].id, "agent", agent)
        try:
            self.predicate.body.execute(c)
        except ReturnException as r:
            return r.value
        return None


class SimulationPredicate:
    def __init__(self, context, predicate) -> None:
        self.context = context
        self.predicate = predicate

    def __call__(self, simulation, *args: Any, **kwds: Any) -> Any:
        c = self.context.get_child()
        c.define_var(self.predicate.param_list[0].id, "simulation", simulation)
        try:
            self.predicate.body.execute(c)
        except ReturnException as r:
            return r.value
        return None


class EmptyPredicate:
    def __init__(self, context, predicate) -> None:
        self.context = context
        self.predicate = predicate

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        c = self.context.get_child()
        try:
            self.predicate.body.execute(c)
        except ReturnException as r:
            return r.value
        return None


def simulate_with_mf(context, args):
    s = args[0].execute(context)
    s_l = args[1].execute(context)
    f_l = args[2].execute(context)
    l = []
    for i, st in enumerate(s_l):
        l.append(evolution.MapFunction(st, AgentPredicate(context, f_l[i])))
    s.simulate(100, None, l, True)


def create_master_simulator(context, args):
    x = args[0].execute(context)
    y = args[1].execute(context)
    rounds = args[2].execute(context)
    days = args[3].execute(context)
    trees = args[4].execute(context)
    return evolution.MasterSimulator(
        dimensions=(x, y), rounds=rounds, days=days, trees=trees
    )


def set_ms_agents_distribution(context, args):
    ms = args[0].execute(context)
    ad = args[1].execute(context)
    ms.agents_distribution = EmptyPredicate(context, ad)


def set_ms_food_distribution(context, args):
    ms = args[0].execute(context)
    fd = args[1].execute(context)
    ms.food_distribution = SimulationPredicate(context, fd)


def run_master_simulator(context, args):
    ms = args[0].execute(context)
    ms.run()


def run_ms_with_mf(context, args):
    ms = args[0].execute(context)
    s_l = args[1].execute(context)
    f_l = args[2].execute(context)
    l = []
    for i, st in enumerate(s_l):
        l.append(evolution.MapFunction(st, AgentPredicate(context, f_l[i])))
    ms.run(plot=1, maping=l)


built_in_functions = {
    "print": p,
    "create_simulator": create_simulator,
    "get_simulation_day": get_simulation_day,
    "create_agent": create_agent,
    "add_agent_to_simulation": add_agent_to_simulation,
    "simulate": simulate,
    "create_world": create_world,
    "get_agent_attr_gene": get_agent_attr_gene,
    "get_agent_value_gene": get_agent_value_gene,
    "set_agent_value_gene": set_agent_value_gene,
    "create_list": create_list,
    "add_elem_to_list": add_elem_to_list,
    "remove_pos_from_list": remove_pos_from_list,
    "create_master_simulator": create_master_simulator,
    "set_ms_agents_distribution": set_ms_agents_distribution,
    "set_ms_food_distribution": set_ms_food_distribution,
    "run_master_simulator": run_master_simulator,
    "simulate_with_mf": simulate_with_mf,
    "set_agent_attr_gene_value": set_agent_attr_gene_value,
    "run_ms_with_mf": run_ms_with_mf,
    "get_simulation_agents_count": get_simulation_agents_count,
}

built_in_fun_type = {
    "print": "Nil",
    "create_simulator": "simulator",
    "get_simulation_day": "number",
    "create_agent": "agent",
    "add_agent_to_simulation": "Nil",
    "simulate": "Nil",
    "create_world": "Nil",
    "get_agent_attr_gene": "number",
    "get_agent_value_gene": "number",
    "set_agent_value_gene": "Nil",
    "create_list": "list",
    "add_elem_to_list": "Nil",
    "remove_pos_from_list": "Nil",
    "create_master_simulator": "master_simulator",
    "set_ms_agents_distribution": "Nil",
    "set_ms_food_distribution": "Nil",
    "run_master_simulator": "Nil",
    "simulate_with_mf": "Nil",
    "set_agent_attr_gene_value": "Nil",
    "run_ms_with_mf": "Nil",
    "get_simulation_agents_count": "number",
}
