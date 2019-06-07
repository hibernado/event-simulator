import sys
import logging
import file_io_utils as fu
import os
import time
from markov import simulate, gen_transition_matrix

logging.basicConfig()
LOG = logging.getLogger()


def main():
    runs = int(sys.argv[1])
    pause_duration = int(sys.argv[2])

    dir_ = os.path.join(fu.get_this_dir(), 'streaming_input')
    fu.delete_dir(dir_)
    fu.make_dir(dir_)

    process = ['homepage',
               'gallery',
               'product_details',
               'basket',
               'checkout',
               'confirmation',
               'account',
               'delivery_status']
    transition_matrix = gen_transition_matrix(len(process))
    entity = 'customer_a'

    while True:

        rows = []
        for a, b in simulate(runs, process, transition_matrix):
            rows.append([entity, a, b])

        path = os.path.join(dir_, fu.get_random_filename())
        fu.write_csv(path, rows)

        time.sleep(pause_duration)

if __name__ == '__main__':
    LOG.setLevel(logging.DEBUG)
    main()
