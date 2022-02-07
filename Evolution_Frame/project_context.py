from multiprocessing import context
from context import Context
from built_in_fun_parse import *

built_in_fun = {
    "create_simulator": create_simulator,
    "get_simulation_day": get_simulation_day,
    "create_world": create_world,
    "create_agent": create_agent,
    "add_agent_to_simulation": add_agent_to_simulation_,
    "simulate": simulate_,
    "new_list": new_list,
    "add_elem_to_list": add_elem_to_list,
    "remove_pos_from_list": remove_pos_from_list,
    "get_agent_value_gene": get_agent_value_gene,
    "create_master_simulator": create_master_simulator,
    "set_ms_agents_distribution": set_ms_agents_distribution,
    "set_ms_food_distribution": set_ms_food_distribution,
    "run_master_simulator": run_master_simulator,
}

built_in_fun_type = {
    "create_simulator": "Simulator",
    "get_simulation_day": "Number",
    "create_world": "Nil",
    "create_agent": "Agent",
    "add_agent_to_simulation": "Nil",
    "simulate": "Nil",
    "new_list": "List",
    "add_elem_to_list": "Nil",
    "remove_pos_from_list": "Nil",
    "get_agent_value_gene": "Number",
    "create_master_simulator": "MasterSimulator",
    "set_ms_agents_distribution": "Nil",
    "set_ms_food_distribution": "Nil",
    "run_master_simulator": "Nil",
}

pc = Context()
pc.infered_id_type = built_in_fun_type
