import numpy as np
from random import choices, randint


def get_next_state(list_):
    ret = [0] * len(list_)
    ret[choices(range(len(list_)), weights=list_)[0]] = 1
    return ret


def get_human_state(states, vector):
    for state, vec in zip(states, vector):
        if vec == 1:
            return state


def simulate(runs, states, transition_matrix):
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
    state_vector = [0] * len(states)
    state_vector[randint(0, len(states)-1)] = 1
    for i in range(runs):

        prev = get_human_state(states, state_vector)
        state_dot_prod_trans = np.dot(state_vector, transition_matrix)
        state_vector = get_next_state(state_dot_prod_trans)
        curr = get_human_state(states, state_vector)

        yield prev, curr


def format_link(source, target):
    return {"source": str(source), "target": str(target)}


def gen_transition_matrix(order):
    transition_matrix = np.random.dirichlet(np.ones(order), size=order)
    return transition_matrix
