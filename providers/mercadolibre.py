from bs4 import BeautifulSoup
import logging
import re
from providers.base_provider import BaseProvider

class Mercadolibre(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source + '_NoIndex_True'
        from_ = 1
        regex = r"(MLA-\d*)"

        while(True):
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)

            if page_response.status_code != 200:
                logging.error(page_response.status_code + ' - ' + page_response.reason)
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('li', class_='ui-search-layout__item')

            if len(properties) == 0:
                break

            for prop in properties:
                section = prop.find('a', class_='ui-search-result__content')
                href = section['href']
                matches = re.search(regex, href)
                internal_id = matches.group(1).replace('-', '')
                price_section = section.find('span', class_='price-tag')
                title_section = section.find('div', class_='ui-search-item__group--title')
                title = title_section.find('span').get_text().strip() + \
                    ': ' + title_section.find('h2').get_text().strip()
                if price_section is not None:
                    title = title + ' ' + price_section.get_text().strip()
        
                yield {
                    'title': title, 
                    'url': href,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                    }

            from_ += 50
            page_link = self.provider_data['base_url'] + source + f"_Desde_{from_}_NoIndex_True"
    