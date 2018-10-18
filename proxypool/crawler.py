import json
import requests
from pyquery import PyQuery as pq

class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if "crawl_" in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1

        attrs['__CrawlFuncCount__'] = count

        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print("get the proxy successfully ", proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        start_url = "http://www.66ip.cn/{}.html"
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print("Crawling ", url)
            html = self.get_page(url)
            if html:
                doc = pq(html)
                trs = doc(".containerbox table tr:gt(0)").items()
                for tr in trs:
                    ip = tr.find("td:nth-child(1)").text()
                    port = tr.find("td:nth-child(2)").text()
                    yield ":".join([ip, port])

    def get_page(self, url):
        html = ""
        try:
            response = requests.get(url)
        except Exception as e:
            print("Bad Request:", e)
            return html
        html = response.text
        return html
