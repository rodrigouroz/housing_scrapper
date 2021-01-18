#import requests
from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider

class Zonaprop(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source + '.html'
        page = 0

        while(True):
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)

            if page_response.status_code != 200:
                break

            page_content = BeautifulSoup(page_response.content, 'lxml')

            paging = page_content.find('div', class_='paging').find('li', class_='active').get_text().strip()
            if page > int(paging):
                break

            properties = page_content.find_all('div', class_='postingCard')

            for prop in properties:
                title = prop.find('a', class_='go-to-posting').get_text().strip()

                logging.debug(title)

                obj = {
                        'title': title,
                        'url': self.provider_data['base_url'] + prop['data-to-posting'],
                        'internal_id': prop['data-id'],
                        'provider': self.provider_name
                }
                logging.debug(obj)
                yield obj

            page += 1
            page_link = self.provider_data['base_url'] + source + f"-pagina-{page}.html"

