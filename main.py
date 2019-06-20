import sys
import logging
import file_io_utils as fu
import os
import time
import math
import asyncio
from markov import simulate, gen_transition_matrix
from config import config
from file_io_utils import make_dir


class BaseSimulator:

    def __init__(self, name):
        super().__init__()

        self.name = name
        self.logger = self._get_logger()
        self.config = Config()

        self.queue = []

    def _get_logger(self):
        logging.basicConfig()
        logger = logging.getLogger(self.name)
        return logger

    def run(self):
        raise NotImplementedError


class Simulator(BaseSimulator):
    def __init__(self, name):
        super().__init__(name)

        self.tasks = []

    async def get_event(self):
        while True:
            self.queue.append(self.get())
            await asyncio.sleep(.1)

    async def put_event(self):
        while True:
            self.put(self.queue)
            self.queue = []
            await asyncio.sleep(3)

    def stop(self):
        for task in self.tasks:
            task.cancel()

    def run(self, duration):
        print('run')
        loop = asyncio.get_event_loop()
        self.tasks.append(loop.create_task(self.get_event()))
        self.tasks.append(loop.create_task(self.put_event()))

        loop.call_later(duration, self.stop)

        try:
            pending = asyncio.Task.all_tasks()
            loop.run_until_complete(asyncio.gather(*pending))
        except asyncio.CancelledError as e:
            print('run cancelled')


class MarkovProcess:

    def __init__(self, process=None, runs_per_iter=None):

        self.process = process
        self.runs_per_iter = runs_per_iter
        self.simulator = simulate

    def _init_matrix(self):
        self.transition_matrix = gen_transition_matrix(len(self.process))

    def init_sim(self, sim, process, runs_per_iter):
        self.process = process
        self.runs_per_iter = runs_per_iter
        self._init_matrix()
        sim.get = self.get_next

    def get_next(self):

        return next(self._simulate())

    def _simulate(self):

        for a, b in self.simulator(self.runs_per_iter,
                                   self.process,
                                   self.transition_matrix):
            yield a, b


# class FabAppSimulator(BaseSimulator):
#
#     def __init__(self, entity, **kwargs):
#         super().__init__(**kwargs)
#         self.entity = entity
#
#     def gen_row(self):
#         for a, b in self._simulate():
#             yield [self.entity, a, b]


class Config(dict):
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def from_object(self, config_object):
        for key in dir(config_object):
            if key.isupper():
                self[key] = getattr(config_object, key)


class BaseStreamer:

    def __init__(self):
        super().__init__()

    def init_sim(self):
        raise NotImplementedError


class FileStreamer(BaseStreamer):
    freq = None
    dir = None

    def __init__(self):
        super().__init__()

    def init_sim(self, sim, dir, freq):
        self.dir = dir
        self.freq = sim.config.get
        # Register streamer with sim
        sim.put = self.write_rows

    def write_rows(self, rows):
        make_dir(self.dir)
        file_name=fu.get_random_filename()
        print('write file: %s' % file_name)
        path = os.path.join(self.dir, file_name)
        fu.write_csv(path, rows)
