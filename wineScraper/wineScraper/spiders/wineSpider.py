from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from ..items import WineItem


def genList(inputList):
    # we want to return a non-empty list so the generated csv columns are aligned
    return inputList if inputList else ['']


class WineSpider(BaseSpider):
    name = "wineSpider"
    allowed_domains = ["wine.com"]
    domain = [
        "http://www.wine.com/",
    ]

    start_urls = [
        "http://www.wine.com/v6/wineshop/list.aspx",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//a[@class="listProductName"]/@href')

        for row in rows:
            url = row.extract()
            fullUrl = self.domain[0] + url
            yield Request(fullUrl, callback=self.parseDetail)

        nextURL = hxs.select('//a[@id="ctl00_BodyContent_ctrProducts_ctrPagingTop_lnkNext').extract()
        if nextURL:
            fullUrl = self.domain[0] + nextURL[0]
            yield Request(fullUrl, callback=self.parse)


    def parseDetail(self, response):
        hxs = HtmlXPathSelector(response)
        wine = WineItem()
        wine['name'] = genList(hxs.select('//h1[@class="detailSubTitle"]/text()').extract())
        wine['price'] = genList(
            hxs.select('//span[@itemprop="lowPrice"]/text() | //span[@itemprop="price"]/text()').extract())
        wine['description'] = genList(
            hxs.select('//p[@id="ctl00_BodyContent_wineMakersNotesContent"]/text()').extract())
        wine['reviews'] = genList(
            hxs.select('//div[@id="criticalAcclaim"]//p[@itemprop="description"]/text()').extract())
        return [wine]
