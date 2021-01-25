from bs4 import BeautifulSoup
import logging
import json
from furl import furl
from providers.base_provider import BaseProvider

class Remax(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        total_pages = 1

        while True:
            if page > total_pages:
                break

            logging.info("Requesting %s" % page_link)
            page_response = self.request(page_link)

            if page_response.status_code != 200:
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            hidden_data = page_content.find('script', id='serverApp-state')
            hidden_json_data = json.loads(hidden_data.text.replace('&q;', '"'))
            properties = hidden_json_data['searchListingDomainKey']['data']

            pagination_items = page_content.select('qr-pagination .mat-ripple.number')
            if page == 1:
                total_pages = len(pagination_items)

            if len(properties) == 0:
                break

            for prop in properties:
                title = prop['title']
                title = title + ' $' + str(prop['price'])
                href = self.provider_data['base_url'] + '/' + prop['slug']
                internal_id = prop['id']

                yield {
                    'title': title,
                    'url': href,
                    'internal_id': internal_id,
                    'provider': self.provider_name
                }

            page += 1
            page_link = self.get_pagination(page_link, page)

    def get_pagination(self, page_link, page_number):
        parsed_listing = furl(page_link)
        parsed_listing.remove(['page', 'pageSize'])
        parsed_listing.add({"page": page_number, "pageSize": 24})
        return parsed_listing.url
        