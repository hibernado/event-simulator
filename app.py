from config import config
from app.sim import Simulator
from app.streams import FileStreamer
from app.markov import MarkovProcess

file_streamer = FileStreamer()
markov_process = MarkovProcess()


def create_sim(config_name):
    sim = Simulator(__name__)
    sim.config.from_object(config[config_name])
    file_streamer.init_sim(sim=sim,
                           dir=sim.config.get('OUTPUT_DIR'),
                           freq=sim.config.get('OUTPUT_FILE_FREQUENCY'))
    markov_process.init_sim(sim=sim,
                            process=sim.config.get('ECOM_PROCESS'),
                            runs_per_iter=sim.config.get('ECOM_RUNS_PER_ITER'))
    return sim


def main(config_name, duration):
    sim = create_sim(config_name)
    sim.run(duration=duration)


if __name__ == '__main__':
    main(config_name='ecom_one_visitor',
         duration=8)
