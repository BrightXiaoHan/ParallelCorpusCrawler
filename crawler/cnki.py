import requests

from typing import Tuple
from crawler.base import BaseCrawler
from bs4 import BeautifulSoup


class CnkiCrawler(BaseCrawler):

    url = "http://dict.cnki.net/dict_result.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Cookie": "ASP.NET_SessionId=0fowo3vqg2hp3l4zolp2vv4u; UM_distinctid=1749b01b425159-0b04ed6f257294-383e570a-1fa400-1749b01b4262ed; CNZZDATA3209959=cnzz_eid%3D1064504841-1592558786-%26ntime%3D1592558786;"
    }

    def _crawl_single(self, seed: str, type: str) -> Tuple[str, str]:
        params = {"scw": seed,
                  "style": "",
                  "tjType": "sentence"}
        response = requests.get(self.url, params=params)
        html = BeautifulSoup(response.text, 'lxml')

        for i in range(3):
            group = html.select('table[id="showjd_%d"]' % i)
            if not group:
                continue
            lines = group[0].select("tr")

            for i in range(2, len(lines), 3):
                item1 = lines[i-2].get_text().strip()
                item2 = lines[i-1].get_text().strip()
                yield [item1, item2]
