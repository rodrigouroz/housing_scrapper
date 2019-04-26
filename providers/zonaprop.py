import requests
from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider

class Zonaprop(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 0

        while(True):
            logging.info(f"Requesting {page_link}")
            page_response = requests.get(page_link)

            if page_response.status_code != 200:
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('li', class_='aviso')

            for prop in properties:
                title = prop.find('a', class_='dl-aviso-a')['title']
                    
                yield {
                    'title': title, 
                    'url': self.provider_data['base_url'] + prop['data-href'],
                    'internal_id': prop['data-aviso'],
                    'provider': self.provider_name
                    }

            page += 1
            page_link = self.provider_data['base_url'] + source + f"--pagina-{page}"
    