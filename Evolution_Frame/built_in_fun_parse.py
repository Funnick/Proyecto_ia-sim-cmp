import evolution
import agent
from typing import Any
from utils import ReturnException


def create_simulator(project_context, args):
    return evolution.Simulator()


def get_simulation_day(project_context, args):
    s = args[0].execute(project_context)
    return s.day


def create_agent(project_context, args):
    return agent.Agent()


def add_agent_to_simulation_(project_context, args):
    s = args[0].execute(project_context)
    s.add_agent_to_simulation(args[1].execute(project_context))


def simulate_(project_context, args):
    s = args[0].execute(project_context)
    s.simulate()


def create_world(project_context, args):
    s = args[0].execute(project_context)
    s.create_world(args[1].execute(project_context), args[2].execute(project_context))


def new_list(project_context, args):
    return []


def add_elem_to_list(project_context, args):
    l = args[0].execute(project_context)
    e = args[1].execute(project_context)
    l.append(e)


def remove_pos_from_list(project_context, args):
    l = args[0].execute(project_context)
    p = args[1].execute(project_context)
    l.pop(p)


class AgentPredicate:
    def __init__(self, context, predicate) -> None:
        self.context = context
        self.predicate = predicate

    def __call__(self, agent, *args: Any, **kwds: Any) -> Any:
        c = self.context.create_child_context()
        c.set_id_value(self.predicate.args[0], agent)
        c.set_infered_id_type(self.predicate.args[0], "Agent")
        try:
            self.predicate.block_stmt.execute(c)
        except ReturnException as r:
            self.type = r.type
            return r.value


class EmptyPredicate:
    def __init__(self, context, predicate) -> None:
        self.context = context
        self.predicate = predicate

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        c = self.context.create_child_context()
        try:
            self.predicate.block_stmt.execute(c)
        except ReturnException as r:
            self.type = r.type
            return r.value


def get_agent_value_gene(project_context, args):
    ag = args[0].execute(project_context)
    gene = args[1].execute(project_context)
    return ag.genetic_code.get_gene(gene).value


def create_master_simulator(project_context, args):
    return evolution.MasterSimulator()


def set_ms_agents_distribution(project_context, args):
    ms = args[0].execute(project_context)
    ad = args[1].execute(project_context)
    ms.agents_distribution = EmptyPredicate(project_context, ad)


def set_ms_food_distribution(project_context, args):
    ms = args[0].execute(project_context)
    fd = args[1].execute(project_context)
    ms.food_distribution = EmptyPredicate(project_context ,fd)


def run_master_simulator(project_context, args):
    ms = args[0].execute(project_context)
    ms.run()


def test(project_context, args):
    s = args[0].execute(project_context)
    p = args[1].execute(project_context)
    ap = AgentPredicate(project_context, p)
    s.simulate(100, None, [evolution.MapFunction("algo", ap)], True)
