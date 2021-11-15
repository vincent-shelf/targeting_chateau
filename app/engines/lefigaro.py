import json
from .engine_model import BaseEngine


class LeFigaroProprietes(BaseEngine):

    MIN_TIME_BEFORE_CALL = 2
    VERBOSITY = 1
    BASE_URL = "https://proprietes.lefigaro.fr/"
    headers = ["ad_url", "link_ref", "price", "description", "characteritics", "ref_advertiser", "location"]

    def get_catalog_page_url(self, nb=1):
        return f"annonces/chateau/?page={nb}"

    def list_catalog_target_pages(self, proc):
        catalog_search_domain =[]
        first_page = proc(self.get_catalog_page_url())
        nb_pages = int(first_page.find("ul", {"class": "pagination"}).findAll("li")[-2].a["data-page"])
        catalog_search_domain += [self.get_catalog_page_url(nb=nb) for nb in range(1, nb_pages+1)]
        print(f"Found {len(catalog_search_domain)} catalog pages to process.")
        return catalog_search_domain

    def extract_adlist_from_catalog_page(self, page_url, page):
        try:
            ad_list = page.findAll("div", {"class": "container-itemlist-inline js-itemlist-inline"})
            return [(page_url, ad['data-href'].replace(self.BASE_URL, "")[1:]) for ad in ad_list]
        except:
            print(f"ERROR while processing catalog page: {page_url}")

    def process_ad_page(self, ad_url, ad_page):
        
        payload = {}

        raw_data = ad_page.find("div", {"id": "js-data"})
        payload['id'] = raw_data['data-id']
        payload['agency_id'] = raw_data['data-agency-id']
        payload['address'] = {
            'region': raw_data['data-tc-region'],
            'departement': raw_data['data-tc-departement'],
            'ville': raw_data['data-tc-ville'],
            'code': raw_data['data-tc-ville-cp'],
            'geoloc': raw_data['data-tc-geoloc'],
            'localisation': raw_data['data-tc-localisation']
        }
        payload['transaction'] = raw_data['data-tc-transaction']
        payload['date_mel'] = raw_data['data-tc-date-mel']

        raw_data2 = ad_page.findAll("script", {"type": "application/ld+json"})
        raw_data2 = [json.loads(t.get_text()) for t in raw_data2]
        raw_data2 = [t for t in raw_data2 if t["@type"]=="Offer"][0]
        payload['url'] = raw_data2['url']
        payload['image'] = raw_data2['image']
        payload['description'] = raw_data2['description']
        payload['priceCurrency'] = raw_data2['priceCurrency']
        payload['price'] = raw_data2['price']
        payload['seller'] = raw_data2['seller']

        specs = {}
        for t in ad_page.find("ul", {"class": "specs-list"}).findAll("li"):
            key = t.find("span", {"class": "specs"}).get_text()
            value = t.find("span", {"class": "specs__values"}).get_text().replace(u'\xa0', u' ')
            specs[key] = value
        payload['features'] = specs

        return payload
