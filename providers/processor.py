import logging
import sqlite3
from providers.zonaprop import Zonaprop
from providers.argenprop import Argenprop
from providers.mercadolibre import Mercadolibre
from providers.properati import Properati
from providers.inmobusqueda import Inmobusqueda
from providers.remax import Remax
from lib.dao import Dao

def process_properties(provider_name, provider_data):
    provider = get_instance(provider_name, provider_data)
    dao = Dao()
    new_properties = []
    for prop in provider.next_prop():
        result = dao.get_property(prop)
        if result == None:
            # Insert and save for notification
            logging.info('It is a new one')
            dao.register_property(prop)
            new_properties.append(prop)
    dao.close()
    return new_properties

def get_instance(provider_name, provider_data):
    # if provider_name == 'zonaprop':
    #     return Zonaprop(provider_name, provider_data)
    # elif provider_name == 'argenprop':
    #     return Argenprop(provider_name, provider_data)
    # elif provider_name == 'mercadolibre':
    #     return Mercadolibre(provider_name, provider_data)
    # elif provider_name == 'properati':
    #     return Properati(provider_name, provider_data)
    # elif provider_name == 'inmobusqueda':
    #     return Inmobusqueda(provider_name, provider_data)
    if provider_name == 'remax':
        return Remax(provider_name, provider_data)
    else:
        raise Exception('Unrecognized provider')
