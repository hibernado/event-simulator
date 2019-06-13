import sys
import logging
import file_io_utils as fu
import os
import time
import math
from markov import simulate, gen_transition_matrix

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

    def run(self, simulator):

        while True:

            rows = []
            for row in simulator.gen_row():
                rows.append(row)

            path = os.path.join(self.dir, fu.get_random_filename())
            fu.write_csv(path, rows)

            time.sleep(self.duration)


def main():
    # runs = int(sys.argv[1])
    # pause_duration = int(sys.argv[2])

    process = ['homepage',
               'gallery',
               'product_details',
               'basket',
               'checkout',
               'confirmation',
               'account',
               'delivery_status']
    sim = FabAppSimulator(entity='customerA', process=process, run_per_iter=10)
    fsim = FileSimulation(dir='./streaming_input', frequency=20)
    fsim.run(sim)


if __name__ == '__main__':
    LOG.setLevel(logging.DEBUG)
    main()
