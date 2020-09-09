from crawler.crawler import ChateauCrawler
from engines.chateauxpourtous import ChateauxPourTous

engine = ChateauxPourTous()

crawler = ChateauCrawler(engine=engine)

crawler.crawl()

print(crawler.show())

crawler.export("../datasets/ChateauxPourTous.csv")
