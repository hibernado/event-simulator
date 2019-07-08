import pytest

import app.sim as sim


def test_config_from_object():
    config = sim.Config()

    class object_:
        lower_case = 1
        UPPER_CASE = 2

    config.from_object(object_)
    assert config.get('lower_case') is None
    assert config.get('UPPER_CASE') == 2


def test_base_simulator():
    sim_ = sim.BaseSimulator('test')
    with pytest.raises(NotImplementedError):
        sim_.run()
    with pytest.raises(NotImplementedError):
        sim_.get()
    with pytest.raises(NotImplementedError):
        sim_.put()


def test_simulator():
    sim_ = sim.Simulator(name='test',
                         get=lambda: 'value',
                         put=lambda x: True
                         )
    sim_.run(0)