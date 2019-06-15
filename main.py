import sys
import logging
import file_io_utils as fu
import os
import time
import math
from markov import simulate, gen_transition_matrix
from config import config

logging.basicConfig()
LOG = logging.getLogger()


class BaseSimulator:

    def __init__(self, process, run_per_iter):
        super().__init__()
        self.process = process
        self.runs_per_iter = run_per_iter

        self.simulator = simulate
        self.transition_matrix = gen_transition_matrix(len(process))

    def _simulate(self):
        for a, b in self.simulator(self.runs_per_iter,
                                   self.process,
                                   self.transition_matrix):
            yield a, b

    def gen_data(self):
        for a, b in self._simulate():
            yield a, b


class FabAppSimulator(BaseSimulator):

    def __init__(self, entity, **kwargs):
        super().__init__(**kwargs)
        self.entity = entity

    def gen_row(self):
        for a, b in self._simulate():
            yield [self.entity, a, b]


class BaseSimulation:
    pass


class FileSimulation(BaseSimulation):
    frequency = None
    dir = None

    def __init__(self, dir, frequency):
        """

        :param dir: target location for files
        :param frequency: number of files to produce per minute
        """
        if not(0 < frequency and frequency <= 60):
            raise ValueError('Frequency arg not in range [1,60]')
        self.frequency = frequency
        self.dir = dir

    @property
    def duration(self):
        return math.ceil(60/self.frequency)

    def set_sim(self, simulator):
        self.simulator = simulator

    def run(self):

        while True:

            rows = []
            for row in self.simulator.gen_row():
                rows.append(row)

            path = os.path.join(self.dir, fu.get_random_filename())
            fu.write_csv(path, rows)

            time.sleep(self.duration)


def create_sim(config_name):

    Config = config[config_name]
    entity = Config.entity
    process = Config.process
    run_per_iter = Config.run_per_iter
    dir = Config.dir
    frequency = Config.frequency
    sim = FabAppSimulator(entity=entity,
                          process=process,
                          run_per_iter=run_per_iter)
    fsim = FileSimulation(dir=dir,
                          frequency=frequency)
    fsim.set_sim(sim)
    return fsim


def main(config_name):

    sim = create_sim(config_name)
    sim.run()



if __name__ == '__main__':
    LOG.setLevel(logging.DEBUG)
    main(sys.argv[1])
