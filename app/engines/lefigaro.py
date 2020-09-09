from app.engines.engine_model import BaseEngine


class LeFigaroProprietes(BaseEngine):

    MIN_TIME_BEFORE_CALL = 2
    VERBOSITY = 1
    BASE_URL = "https://proprietes.lefigaro.fr/"
    headers = ["ad_url", "link_ref", "price", "description", "characteritics", "ref_advertiser", "location"]

    def get_catalog_page_url(self, nb=1):
        return f"{self.base_url}/annonces/chateau/?page={nb}"

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
            return [(page_url, ad.a['href'].replace(self.BASE_URL, "")) for ad in ad_list]
        except:
            print(f"ERROR while processing catalog page: {page_url}")

    def process_ad_page(self, ad_url, ad_page):

        # link ref
        link_ref = ad_page.find("link", {"rel": "canonical"})

        # price
        price = ad_page.find("span", {"class": "nb-price"})

        # stats
        # TODO detail
        for t in ad_page[0].findAll("span", {"class": "nb"}):
            print(t.get_text())

        # desc
        description = ad_page.findAll("p", {"id": "js-description", "itemprop": "description"})

        # caracteristiques
        characteritics = ad_page.findAll("div", {"class": "caracteristiques"})[0].findAll("p", {"class": "h2-like"})

        #ref annonceur
        ref_advertiser = ad_page.findAll("p", {"class": "ref-annonce"})

        # geoloc
        location = ad_page.findAll("span", {"class": "name", "itemprop": "addressLocality"})[0].get_text()

        return [ad_url, link_ref, price, description, characteritics, ref_advertiser, location]
