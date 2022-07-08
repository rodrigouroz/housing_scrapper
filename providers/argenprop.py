from bs4 import BeautifulSoup
import logging
import re
from providers.base_provider import BaseProvider

class Argenprop(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 0
        regex = r".*--(\d+)"

        while(True):
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)
            
            if page_response.status_code != 200:
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('div', class_='listing__item')

            if len(properties) == 0:
                break

            for prop in properties:
                title = prop.find('p', class_='card__title')
                price_section = prop.find('p', class_='card__price')
                if price_section is not None:
                    title = title.get_text().strip() + ' ' + price_section.get_text().strip()
                href = prop.find('a', class_='card')['href']
                matches = re.search(regex, href)
                internal_id = matches.group(1)
                    
                yield {
                    'title': title, 
                    'url': self.provider_data['base_url'] + href,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                    }

            page += 1
            page_link = self.provider_data['base_url'] + source + f"-pagina-{page}"
