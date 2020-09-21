import requests

from typing import List, Iterable
from crawler.base import BaseCrawler
from bs4 import BeautifulSoup


class CnkiCrawler(BaseCrawler):

    url = "http://dict.cnki.net/dict_result.aspx"

    def _crawl_single(self, seed: str, type: str) -> Iterable[List[str]]:
        params = {"scw": seed,
                  "style": "",
                  "tjType": "sentence"}
        response = requests.get(self.url, params=params, timeout=2)
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
