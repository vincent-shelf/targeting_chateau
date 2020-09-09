from crawler.crawler import ChateauCrawler
from engines.chateauxpourtous import ChateauxPourTous

engine = ChateauxPourTous()

crawler = ChateauCrawler(engine=engine)

dataset = crawler.crawl()
