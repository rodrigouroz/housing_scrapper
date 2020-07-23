import logging
import yaml
from providers.zonaprop import Zonaprop
from providers.argenprop import Argenprop
from providers.mercadolibre import Mercadolibre
from providers.properati import Properati

if __name__ == "__main__":
    # logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    with open("../configuration.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    provider = Zonaprop('zonaprop', cfg['providers']['zonaprop'])
    [print(prop) for prop in provider.next_prop()]

    provider = Argenprop('argenprop', cfg['providers']['argenprop'])
    [print(prop) for prop in provider.next_prop()]

    provider = Mercadolibre('mercadolibre', cfg['providers']['mercadolibre'])
    [print(prop) for prop in provider.next_prop()]

    provider = Properati('properati', cfg['providers']['properati'])
    [print(prop) for prop in provider.next_prop()]

