import requests, time, datetime
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3


class ChateauCrawler:

    result_df = []

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
            # print(f"Page loaded successfully")
            return self.engine.process_ad_page(ad_url, ad_page)
        except Exception as e:
            print(f"Processing failed for ad page call {ad_url} with error {str(e)}")
            return []

    def crawl(self):
        print(f"Starting crawler at {str(datetime.datetime.now())}")
        complete_ad_list = self.extract_complete_ad_list()

        print(f"Starting collecting all {len(complete_ad_list)} ads at {str(datetime.datetime.now())}")
        crawl = []
        for ad_url in complete_ad_list:
            crawl += [self.collect_ad(ad_url[1])]

        print(f"Done collecting all {len(complete_ad_list)} ads at {str(datetime.datetime.now())}")
        # self.result_df = pd.DataFrame(crawl, columns=self.engine.headers)
        print(crawl)
        self.result_df = pd.json_normalize(crawl)
        print(self.result_df )

    def show(self):
        print(self.result_df)


    def export_to_csv(self, target_path):
        print(f"Exporting file started at {str(datetime.datetime.now())}")
        self.result_df.to_csv(target_path, index=False)
        print(f"Exporting file finished at {str(datetime.datetime.now())}")

    def export(self, target_db, target_table):
        con = sqlite3.connect(target_db)
        print(f"Exporting file started at {str(datetime.datetime.now())}")
        self.result_df.to_sql(target_table, con, if_exists="replace")
        con.close()
        print(f"Exporting file finished at {str(datetime.datetime.now())}")




