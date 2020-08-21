#import requests
from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider

class Zonaprop(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 0

        while(True):
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)
            
            if page_response.status_code != 200:
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('div', class_='posting-card')

            for prop in properties:
                title = prop.find('a', class_='go-to-posting').get_text().strip()
                price_section = prop.find('span', class_='first-price')
                if price_section is not None:
                    title = title + ' ' + price_section['data-price']
                    
                yield {
                    'title': title, 
                    'url': self.provider_data['base_url'] + prop['data-to-posting'],
                    'internal_id': prop['data-id'],
                    'provider': self.provider_name
                    }

            page += 1
            page_link = self.provider_data['base_url'] + source + f"--pagina-{page}"
    