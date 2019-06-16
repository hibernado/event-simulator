from config import config
from main import Simulator, FileStreamer

file_streamer = FileStreamer()


def create_sim(config_name):
    sim = Simulator(__name__)
    sim.config.from_object(config[config_name])
    file_streamer.init_sim(sim)
    return sim


def main(config_name):
    sim = create_sim(config_name)
    sim.run()


if __name__ == '__main__':
    main('ecom_one_visitor')
