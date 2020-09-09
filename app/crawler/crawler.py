import requests, time, datetime
from bs4 import BeautifulSoup


class ChateauCrawler:

    def __init__(self, engine):
        self.engine = engine
        self.base_url = engine.BASE_URL
        self.sleep_time = engine.MIN_TIME_BEFORE_CALL
        self.verbosity = engine.VERBOSITY

    def process_page(self, url):
        time.sleep(self.sleep_time)
        if self.verbosity==1:
            print(f"-- Calling {url}")
        page = requests.get(f"{self.base_url}/{url}")
        return BeautifulSoup(page.content, 'html.parser')

    def extract_complete_ad_list(self):
        catalog_search_domain = self.engine.list_catalog_target_pages(self.process_page)
        ad_list = []
        for catalog_page in catalog_search_domain:
            ad_list += self.engine.extract_adlist_from_catalog_page(catalog_page, self.process_page(catalog_page))
        print(f"Found {len(ad_list)} ads to process.")
        return ad_list

    def collect_ad(self, ad_url):
        try:
            ad_page = self.process_page(ad_url)
            return self.engine.process_ad_page(ad_url, ad_page)
        except Exception as e:
            print(f"Processing failed for ad page call {ad_url}")

    def crawl(self):
        complete_ad_list = self.extract_complete_ad_list()
        crawl = []
        print(f"Starting collecting all {len(complete_ad_list)} ads at {str(datetime.datetime.now())}")
        for ad_url in complete_ad_list:
            crawl += self.collect_ad(ad_url)
        return crawl
