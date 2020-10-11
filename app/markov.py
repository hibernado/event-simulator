import random as rnd

import numpy as np


def get_next_state(list_):
    ret = [0] * len(list_)
    ret[rnd.choices(range(len(list_)), weights=list_)[0]] = 1
    return ret


def get_human_state(states, vector):
    for state, vec in zip(states, vector):
        if vec == 1:
            return state


def simulate(runs, states, transition_matrix, seed=None):
    """
    Run a simulation using a markov model
    transition_matrix = [[0.2, 0.6, 0.1, 0.1],
                         [0.1, 0.1, 0.7, 0.1],
                         [0.25, 0.25, 0.25, 0.25],
                         [0.2, 0.3, 0.3, 0.2]]

    process = ['homepage', 'gallery', 'product_details', 'checkout']

    for a, b in simulate(50, process, transition_matrix):
        print(format_link(a, b))
    """
    if seed is not None:
        rnd.seed(seed)
    state_vector = [0] * len(states)
    state_vector[rnd.randint(0, len(states) - 1)] = 1
    for i in range(runs):
        prev = get_human_state(states, state_vector)
        state_dot_prod_trans = np.dot(state_vector, transition_matrix)
        state_vector = get_next_state(state_dot_prod_trans)
        curr = get_human_state(states, state_vector)

        yield prev, curr


def gen_transition_matrix(order, seed=None):
    if seed is not None:
        np.random.seed(seed)
    transition_matrix = np.random.dirichlet(np.ones(order), size=order)
    return transition_matrix


class MarkovProcess:

    def __init__(self, process=None, runs_per_iter=None, format=None,
                 seed=None):

        self.process = process
        self.runs_per_iter = runs_per_iter
        self.simulator = simulate
        if process:
            self._init_matrix(seed)
        if format:
            self._init_formatter(format)

    def _init_matrix(self, seed=None):
        self.transition_matrix = gen_transition_matrix(len(self.process), seed)

    def _formatter_tuple(self, x, y):
        return x, y

    def _formatter_indexed_tuple(self, x, y):
        return (self.process.index(x), x,), (self.process.index(y), y,)

    def _formatter_dict(self, x, y):
        return {"source": x, "target": y}

    def _init_formatter(self, format):

        if format == 'tuple':
            self.format = self._formatter_tuple
        elif format == 'indexed-tuple':
            self.format = self._formatter_indexed_tuple
        elif format == 'dict':
            self.format = self._formatter_dict

    def init_sim(self, sim):
        sim.get = self.get_next

    def get_next(self, seed=None):
        a, b = next(self._simulate(seed))
        return self.format(a, b)

    def _simulate(self, seed=None):

        for a, b in self.simulator(self.runs_per_iter,
                                   self.process,
                                   self.transition_matrix,
                                   seed):
            yield a, b
