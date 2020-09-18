import datetime
from app.crawler.crawler import ChateauCrawler
from app.engines.chateauxpourtous import ChateauxPourTous
from app.engines.lefigaro import LeFigaroProprietes

CONFIGS = [
    {
        "name": "LeFigaroProprietes",
        "engine": LeFigaroProprietes,
        "database": "../datasets/chateaux_v1.sqlite",
        "target_table": "LeFigaroProprietes",
    },
    {
        "name": "ChateauxPourTous",
        "engine": ChateauxPourTous,
        "database": "../datasets/chateaux_v1.sqlite",
        "target_table": "ChateauxPourTous",
    }
]

for eng in CONFIGS:
    start_time = datetime.datetime.now()
    print(f"Starting processing {eng['name']} at {str(start_time)}")
    engine = eng["engine"]()
    crawler = ChateauCrawler(engine=engine)

    crawler.crawl()
    print(f"Exporting results of {eng['name']} at {str(datetime.datetime.now())}")
    crawler.export(target_db=eng["database"], target_table=eng["target_table"])
    print(f"Finishing {eng['name']} at {str(datetime.datetime.now())} after {str(datetime.datetime.now()-start_time)}")

