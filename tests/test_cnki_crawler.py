import os

from crawler.cnki import CnkiCrawler

cwd = os.path.dirname(__file__)

crawler = CnkiCrawler.from_excel(os.path.join(cwd, "./assets/dict.xlsx"))
crawler.crawl()
crawler.save("result.xlsx")
