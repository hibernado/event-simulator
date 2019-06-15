class Config:
    pass


class EcommerceUserConfig(Config):
    process = ['homepage',
               'gallery',
               'product_details',
               'basket',
               'checkout',
               'confirmation',
               'account',
               'delivery_status']

    entity = 'CustomerA'
    run_per_iter = 20
    dir = './streaming_input'
    frequency = 20


config = {
    'ecom_user': EcommerceUserConfig
}
