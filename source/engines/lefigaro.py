import requests
from bs4 import BeautifulSoup

BASE_URL = "https://proprietes.lefigaro.fr/"


class ChateauCrawler:

    def __init__(self):
        self.base_url = BASE_URL

    def process_page(self, url):
        page = requests.get(url)
        return BeautifulSoup(page.content, 'html.parser')

    def get_catalog_page_url(self, nb=1):
        return f"{self.base_url}/annonces/chateau/?page={nb}"

    def get_ad_page_url(self, ad_path):
        return f"{self.base_url}/{ad_path}"

    def catalog_get_list_ads(self, page_nb=1):
        soup = self.process_page(self.get_catalog_page_url(page_nb))
        list = soup.findAll("div", {"class": "container-itemlist-inline js-itemlist-inline"})
        return [ad.a['href'] for ad in list]

    def reload_ad_list(self):
        first_page = self.process_page(self.get_catalog_page_url())
        nb_pages = int(first_page.find("ul", {"class": "pagination"}).findAll("li")[-2].a["data-page"])
        complete_ad_list = []
        for i in range(1, nb_pages+1):
            print(f"Fetching catalog page {i}")
            complete_ad_list += self.catalog_get_list_ads(page_nb=i)
            if i>5:
                break
        print(complete_ad_list)

    def list_ad(self, ad_url):
        soup = self.process_page(self.get_ad_page_url(ad_url))
        # link ref
        link_ref = soup.find("link", {"rel": "canonical"})

        # price
        price = soup.find("span", {"class": "nb-price"})

        # stats
        # TODO detail
        for t in lol[0].findAll("span", {"class": "nb"}):
            print(t.get_text())

        # desc
        description = soup.findAll("p", {"id": "js-description", "itemprop": "description"})

        # caracteristiques
        characteritics = soup.findAll("div", {"class": "caracteristiques"})[0].findAll("p", {"class": "h2-like"})

        #ref annonceur
        ref_advertiser = soup.findAll("p", {"class": "ref-annonce"})

        # geoloc
        location = soup.findAll("span", {"class": "name", "itemprop": "addressLocality"})[0].get_text()

        return link_ref, price, description, characteritics, ref_advertiser, location


lol = ChateauCrawler()

lol.reload_ad_list()
