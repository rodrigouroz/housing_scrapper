import requests
from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider

class Mercadolibre(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source + '_NoIndex_True'
        from_ = 1

        while(True):
            logging.info(f"Requesting {page_link}")
            page_response = requests.get(page_link)

            if page_response.status_code != 200:
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('li', class_='results-item')

            if len(properties) == 0:
                break

            for prop in properties:
                internal_id = prop.find('div', class_='rowItem')['id']
                section = prop.find('a', class_='item__info-link')
                href = section['href']
                title = section.find('div', class_='item__title').get_text().strip()
                    
                yield {
                    'title': title, 
                    'url': href,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                    }

            from_ += 50
            page_link = self.provider_data['base_url'] + source + f"_Desde_{from_}_NoIndex_True"
    