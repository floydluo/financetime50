
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst
from scrapy import Spider
from scrapy.http import Request



class TestSpider(Spider):
    name = 'dsstest'
    start_urls = (
            "http://www.journals.elsevier.com/decision-support-systems/",
            )
    parsed_urls = []
    base_url = "http://www.sciencedirect.com/science/journal/01679236/"

    def parse(self, response):
        url = self.base_url +'1'
        meta = {'v':1}
        yield Request(url, meta = meta, callback =self.parse_volume)

    def parse_volume(self,response):
        if response.status == 200:
            self.parsed_urls.append(response.url)

            article_xpath = '//ol[@class="articleList results"]//a[@class="cLink artTitle S_C_artTitle "]/@href'


            print("From: ", response.url,'------------  < --  (* _ *')

            n = 0
            for docurl in response.xpath(article_xpath).extract():
                if docurl not in self.parsed_urls:
                    n += 1
                    self.parsed_urls.append(docurl)
                    print(docurl)


            url = response.url + '/1'
            if url not in self.parsed_urls:
                self.parsed_urls.append(url)
                yield Request(url, callback = self.parse_issue)

            response.meta['v'] += 1
            url = self.base_url + str(response.meta['v'])
            if url not in self.parsed_urls:
                self.parsed_urls.append(url)
                yield Request(url, meta= response.meta, callback = self.parse_volume)


    def parse_issue(self, response):
        if response.status == 200:
            ## the same codes in parse_issue method.
            article_xpath = '//ol[@class="articleList results"]//a[@class="cLink artTitle S_C_artTitle "]/@href'

            print("From: ", response.url,'------------  < --  (* _ *')
            n = 0
            for docurl in response.xpath(article_xpath).extract():
                if docurl not in self.parsed_urls:
                    n +=1
                    self.parsed_urls.append(docurl)
                    print(docurl)

            url = response.url[:-1] + str(int(response.url[-1])+1)


            if url not in self.parsed_urls and n != 0:
                self.parsed_urls.append(url)
                yield Request(url, callback = self.parse_issue)
