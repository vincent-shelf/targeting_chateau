BASE_URL_CATEGORY = [
    "France-1-achat-vente-maison-bourgeoise-de-charme-ancien-presbytere-chapelle-pas-chere-a-restaurer-a-vendre-france",
    "France-2-achat-vente-belle-demeure-ancienne-de-caractere-de-charme-a-vendre-france",
    "France-3-achat-vente-manoir-maison-de-maitre-presbytere-chapelle-prieure-a-vendre-france",
    "France-4-achat-vente-chateau-haras-domaine-demeure-de-prestige-de-luxe-a-vendre-france"
]


class ChateauxPourTous(EngineModel):

    MIN_TIME_BEFORE_CALL = 2
    VERBOSITY = 1
    BASE_URL = "http://www.chateauxpourtous-classique.fr"

    @override
    def get_catalog_page_url(self, target=BASE_URL_CATEGORY[0], nb=1):
        return f"{target}-page{nb}.php" if nb>1 else f"{target}.php"

    def list_catalog_target_pages(self, proc):
        import re
        catalog_search_domain =[]
        for category in BASE_URL_CATEGORY:
            first_page = proc(self.get_catalog_page_url(target=category))
            l = first_page.findAll("img", {"src": lambda L: L and L.startswith('numero/')})
            nb_pages = max([int(x[0]) for x in [re.findall(r'\d+|$', i['src']) for i in l] if x[0] != ''])
            catalog_search_domain += [self.get_catalog_page_url(target=category, nb=nb) for nb in range(1, nb_pages+1)]
        print(f"Found {len(catalog_search_domain)} catalog pages to process.")
        return catalog_search_domain

    def extract_adlist_from_catalog_page(self, page_url, page):
        try:
            ad_list = page.findAll("div", {"class": "absolubiens"})
            return [(page_url, ad.a['href'].replace(self.BASE_URL, "")) for ad in ad_list]
        except:
            print(f"ERROR while processing catalog page: {page_url}")

    def process_ad_page(self, ad_url, ad_page):

        # title
        title = ad_page.find("h2").text

        # price
        price = ad_page.find("h1").text

        # desc
        description = ad_page.find("h4").text

        #ref annonceur eg. "Référence de l'annonce : 16878"
        #ref_advertiser = soup.findAll("p", {"class": "ref-annonce"})

        img_list = [i["src"] for i in ad_page.findAll("img", {"src": lambda L: L and L.startswith('selectionhabitat')})]

        return [ad_url, title, price, description, img_list]
