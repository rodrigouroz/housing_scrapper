from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider
import re

class Lavoz(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1

        while(True):
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)

            page_content = BeautifulSoup(page_response.content, 'lxml')
            next_page = page_content.find_all('a', class_=re.compile('right button-narrow'))
            logging.debug(next_page)
            if len(next_page) < 1:
                break

            properties = page_content.find_all('div', class_=re.compile('flex col col-12 my2'))

            for prop in properties:
                url = prop.find('a', class_='text-decoration-none')['href']
                title = prop.find('div', class_='title-2lines-list')
                price_section = prop.find('p', class_=re.compile('main bold mb0 mt0 h2 flex'))
                internal_id = prop.find('amp-state')['id']

                obj = {
                    'title': title.get_text().strip(),
                    'url': url,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                    }
                yield obj

            page += 1
            page_link = self.provider_data['base_url'] + source + f"&page={page}"

