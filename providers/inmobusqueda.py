from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider

class Inmobusqueda(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1

        while True:
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)

            if page_response.status_code != 200:
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('div', class_='ResultadoCaja')

            for prop in properties:
                link = prop.find('div', class_='resultadoTipo').find('a')
                href = link['href']

                if len(properties) == 1 and href == '#':
                    return

                title = link.get_text().strip()
                price_section = prop.find('div', class_='resultadoPrecio')
                if price_section is not None:
                    title = title + ' ' + price_section.get_text().strip()
                
                internal_id = prop.find('div', class_='codigo').get_text().strip()
                yield {
                    'title': title, 
                    'url': href,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                    }

            page += 1
            page_link = self.provider_data['base_url'] + source.replace(".html", f"-pagina-{page}.html")
