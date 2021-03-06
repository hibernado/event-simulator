import asyncio
import logging


class Config(dict):
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def from_object(self, config_object):
        for key in dir(config_object):
            if key.isupper():
                self[key] = getattr(config_object, key)


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

    def get(self):
        raise NotImplementedError

    def put(self):
        raise NotImplementedError


class Simulator(BaseSimulator):
    def __init__(self, name, get=None, put=None):
        super().__init__(name)
        self.get = get
        self.put = put
        self.tasks = []

    async def get_event(self):
        while True:
            async for event in self.get():
                self.queue.append(event)
            await asyncio.sleep(.0000001)

    async def flush_events(self):
        while True:
            await self.put(self.queue)
            self.queue = []
            await asyncio.sleep(3)

    def stop(self):
        for task in self.tasks:
            task.cancel()

    def run(self, duration):
        print('run')
        loop = asyncio.get_event_loop()
        self.tasks.append(loop.create_task(self.get_event()))
        self.tasks.append(loop.create_task(self.flush_events()))

        loop.call_later(duration, self.stop)

        try:
            pending = asyncio.Task.all_tasks()
            loop.run_until_complete(asyncio.gather(*pending))
        except asyncio.CancelledError:
            print('run cancelled')
