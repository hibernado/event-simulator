class Config:
    pass

    @staticmethod
    def init_sim(sim):
        pass


class EcommerceUserConfig(Config):
    SIMULATOR_TYPE = 'one_ecommerce_visitor'

    ECOM_PROCESS = ['homepage',
                    'gallery',
                    'product_details',
                    'basket',
                    'checkout',
                    'confirmation',
                    'account',
                    'delivery_status']
    #
    # ECOM_ENTITY = 'CustomerA'
    ECOM_RUNS_PER_ITER = 10
    ECOM_PROCESS_OUTPUT_FORMAT = 'indexed-tuple'
    #
    # OUTPUT_TYPE = 'file'
    OUTPUT_DIR = './streaming_input'
    OUTPUT_FILE_FREQUENCY = 60
    OUTPUT_FILE_DELIMITER = "|"

    @classmethod
    def init_sim(sim):
        import sys
        import logging

        logging.StreamHandler(sys.stdout)


config = {
    'ecom_one_visitor': EcommerceUserConfig
}
