import pytest
from app.markov import MarkovProcess


def test_markov_process_no_args_get_next():
    mark = MarkovProcess()
    with pytest.raises(Exception) as e:
        mark.get_next()


def test_markov_process_args_get_next():
    mark = MarkovProcess(process=['a','b','c'],
                         runs_per_iter=1)
    mark.get_next()

