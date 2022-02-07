from typing import Iterable, Set, List


SYMBOL_TABLE = list(map(chr, range(128)))


class State:
    count = 0

    def __init__(self) -> None:
        State.count = State.count + 1
        self._id = State.count
        self._is_final = False

    def __eq__(self, __o: object) -> bool:
        return self._id == __o._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __str__(self) -> str:
        return str(self._id)


class StatesHash:
    def __init__(self, states: Iterable[State]) -> None:
        self._states = states

    def __hash__(self) -> int:
        sum = 0
        for st in self._states:
            sum = sum + st.__hash__()

        return hash(sum)

    def __eq__(self, __o: object) -> bool:
        return self._states == __o._states

    @property
    def states(self):
        return self._states


class FiniteState(State):
    def __init__(self, states_represented) -> None:
        id_sum = 0
        for i, st in enumerate(states_represented):
            id_sum = id_sum + ((i + 1) * st._id)
        self._id = id_sum
        self._is_final = False
        self._states_represented = states_represented

    def __eq__(self, __o: object) -> bool:
        return (
            self._id == __o._id and self._states_represented == __o._states_represented
        )

    def __hash__(self) -> int:
        return hash(self._id)

    @property
    def states_repr(self):
        return self._states_represented


class Transition:
    def __init__(self, head_state: State, symbol, body_state: State) -> None:
        self._head_state = head_state
        self._symbol = symbol
        self._body_state = body_state

    @property
    def head_state(self) -> State:
        return self._head_state

    @property
    def symbol(self):
        return self._symbol

    @property
    def body_state(self) -> State:
        return self._body_state


class TransitionFunction:
    def __init__(self, transitions: List[Transition]) -> None:
        self.funct = {}
        for t in transitions:
            if self.funct.get(t.head_state):
                self.funct[t.head_state].append(t)
            else:
                self.funct[t.head_state] = [t]

    @property
    def transitions(self):
        l = []
        for v in self.funct.values():
            for i in v:
                l.append(i)
        return l

    def get_symbol_transitions_of(self, state: State, char: str):
        symbol_transitions = []

        transitions = self.funct.get(state)
        if transitions == None:
            return symbol_transitions
        for t in transitions:
            if t.symbol == char:
                symbol_transitions.append(t)

        return symbol_transitions

    def get_eps_transitions_of(self, state: State):
        eps_transitions = []

        transitions = self.funct.get(state)
        if transitions == None:
            return eps_transitions
        for t in transitions:
            if t.symbol == "eps":
                eps_transitions.append(t)

        return eps_transitions


class Automata:
    def __init__(
        self,
        states,
        initial_state,
        symbols,
        final_states,
        transition_function,
    ) -> None:
        self._states = states
        self._initial_state = initial_state
        self._symbols = symbols
        self._final_states = final_states
        self._transition_function = transition_function

        for st in states:
            st._is_final = False
        for st in self._final_states:
            st._is_final = True

        self.current_state = self._initial_state
        self.sequence_states = [self.current_state]
        self._special_state = FiniteState([State()])

    def _eps_closure(self, states: Set[State]) -> Set[State]:
        eps_closure_list = states.copy()
        stack = list(states)

        while len(stack) > 0:
            top_state = stack.pop()
            for transition in self._transition_function.get_eps_transitions_of(
                top_state
            ):
                if transition.body_state not in eps_closure_list:
                    eps_closure_list.add(transition.body_state)
                    stack.append(transition.body_state)

        return eps_closure_list

    def _move(self, states: Iterable[State], char: str) -> Set[State]:
        trans_states_with_char = set([])

        for st in states:
            for transition in self._transition_function.get_symbol_transitions_of(
                st, char
            ):
                trans_states_with_char.add(transition.body_state)

        return trans_states_with_char

    def match_one_char(self, character: str):
        self.current_state = self._advance(self.current_state, character)
        if self.current_state is not None:
            self.sequence_states.append(self.current_state)
        else:
            self.sequence_states.append(self._special_state)
        return self.current_state

    def reset(self):
        self.current_state = self._initial_state
        self.sequence_states = [self.current_state]

    def _advance(self, state, char):
        t = self._transition_function.get_symbol_transitions_of(state, char)
        if len(t) == 1:
            return t[0].body_state

        return None

    def simulate(self, string):
        state = self._initial_state
        for c in string:
            state = self._advance(state, c)
            if not state:
                return False
        return state._is_final


def convert_NFA_in_DFA(nfa):
    eps_closure = nfa._eps_closure(set([nfa._initial_state]))

    dfa_initial_state = FiniteState(eps_closure)
    dfa_states = set([dfa_initial_state])
    dfa_final_states = set([])
    transition_list = []

    dict_id_fs = {dfa_initial_state._id: dfa_initial_state}

    for st in eps_closure:
        if st._is_final:
            dfa_final_states.add(dfa_initial_state)
            break

    unmarked_states = [dfa_initial_state]
    while len(unmarked_states) > 0:
        T = unmarked_states.pop()

        for symbol in nfa._symbols:
            U = nfa._eps_closure(nfa._move(T.states_repr, symbol))
            if len(U) == 0:
                continue
            fs_temp = FiniteState(U)
            if fs_temp not in dfa_states:
                dict_id_fs[fs_temp._id] = fs_temp
                unmarked_states.append(fs_temp)
                dfa_states.add(fs_temp)
                for st in U:
                    if st._is_final:
                        dfa_final_states.add(fs_temp)
            transition_list.append(Transition(T, symbol, dict_id_fs[fs_temp._id]))

    return Automata(
        dfa_states,
        dfa_initial_state,
        nfa._symbols,
        dfa_final_states,
        TransitionFunction(transition_list),
    )


def automata_union(fst_nfa, snd_nfa):
    new_initial_state = State()
    new_final_state = State()

    new_transitions = [
        Transition(new_initial_state, "eps", fst_nfa._initial_state),
        Transition(new_initial_state, "eps", snd_nfa._initial_state),
        Transition(fst_nfa._final_states[0], "eps", new_final_state),
        Transition(snd_nfa._final_states[0], "eps", new_final_state),
    ]

    states = [new_initial_state, new_final_state]
    states.extend(fst_nfa._states)
    states.extend(snd_nfa._states)

    new_transitions.extend(fst_nfa._transition_function.transitions)
    new_transitions.extend(snd_nfa._transition_function.transitions)

    return Automata(
        states,
        new_initial_state,
        fst_nfa._symbols,
        [new_final_state],
        TransitionFunction(new_transitions),
    )


def automata_concat(fst_nfa, snd_nfa):
    new_transitions = [
        Transition(fst_nfa._final_states[0], "eps", snd_nfa._initial_state)
    ]
    new_transitions.extend(fst_nfa._transition_function.transitions)
    new_transitions.extend(snd_nfa._transition_function.transitions)

    states = []
    states.extend(fst_nfa._states)
    states.extend(snd_nfa._states)

    return Automata(
        states,
        fst_nfa._initial_state,
        fst_nfa._symbols,
        snd_nfa._final_states,
        TransitionFunction(new_transitions),
    )


def automata_closure(nfa):
    new_initial_state = State()
    new_final_state = State()

    new_transitions = [
        Transition(new_initial_state, "eps", nfa._initial_state),
        Transition(new_initial_state, "eps", new_final_state),
        Transition(nfa._final_states[0], "eps", new_final_state),
        Transition(nfa._final_states[0], "eps", nfa._initial_state),
    ]
    new_transitions.extend(nfa._transition_function.transitions)

    states = [new_initial_state, new_final_state]
    states.extend(nfa._states)

    return Automata(
        states,
        new_initial_state,
        nfa._symbols,
        [new_final_state],
        TransitionFunction(new_transitions),
    )
