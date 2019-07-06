import numpy as np
import pytest

from app.markov import MarkovProcess, gen_transition_matrix
from app.sim import Simulator


def test_gen_transition_matrix():
    mat = gen_transition_matrix(order=2, seed=0)
    expected = np.array([[0.38788988, 0.61211012], [0.53976265, 0.46023735]])
    assert np.allclose(expected, mat)


def test_markov_process_no_args():
    mark = MarkovProcess()
    with pytest.raises(Exception):
        mark.get_next()


def test_markov_process_args():
    mark = MarkovProcess(process=['a', 'b', 'c'],
                         runs_per_iter=1,
                         format='tuple')
    mark.get_next()


def test_markov_process_init_sim_args():
    mark = MarkovProcess()
    sim = Simulator('test_sim')
    mark.init_sim(sim=sim,
                  process=['a', 'b', 'c'],
                  runs_per_iter=1,
                  format='indexed-tuple')
    mark.get_next()


def test_tuple_format():
    mark = MarkovProcess(process=['a', 'b', 'c'],
                         runs_per_iter=1,
                         format='tuple',
                         seed=0)
    out = mark.get_next(seed=0)
    assert out == ('b', 'c')


def test_index_tuple_format():
    mark = MarkovProcess(process=['a', 'b', 'c'],
                         runs_per_iter=1,
                         format='indexed-tuple',
                         seed=0)
    out = mark.get_next(seed=0)
    assert out == ((1, 'b'), (2, 'c'))


def test_dict_format():
    mark = MarkovProcess(process=['a', 'b', 'c'],
                         runs_per_iter=1,
                         format='dict',
                         seed=0)
    out = mark.get_next(seed=0)
    assert out == {"source": 'b', "target": 'c'}
