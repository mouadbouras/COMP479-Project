import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import io
import re
import html2text

class Spyder(scrapy.Spider):
    name = "Spyder"
    start_urls = ["http://csu.qc.ca/content/student-groups-associations"]

    def __init__(self, max=10, docID=1, corpusID=1):
        self.COUNT = 0;
        self.MAX = int(max)
        self.ID = int(docID)
        self.CORPUS = int(corpusID)
        self.URLS = [
            "http://cufa.net/",
            "http://www.cupfa.org/",
            "http://www.concordia.ca/artsci/students/associations.html"
        ]
        

    # def start_requests(self):
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hxs = Selector(response)
        title = hxs.xpath('//title').extract()
        body = hxs.xpath('//body').extract()

        # noHTMLRegex = re.compile('(<.*?>)|<.*?>.*?</script>|<.*?>.*?</style>|&.*?;|<.*?>.*?</iframe>|<!--.*?-->')
        # body[0] = re.sub(noHTMLRegex, ' ', body[0])
        # title[0] = re.sub(noHTMLRegex, ' ', title[0])

        h = html2text.HTML2Text()
        h.ignore_links = True
        body[0] = h.handle(body[0])
        title[0] = h.handle(title[0])

        extracted = title[0] + '\n' + body[0]
        fileName = str(self.CORPUS) + ".txt"


        # if()
        #     self.CORPUS += 1

        corpusTitle = '<document id="' + str(self.ID) + '" url= "' + response.url + '">'
        self.ID += 1
        corpusEnd = "</document>"

        with io.open(fileName, "a", encoding="utf-8") as f:
            f.write(corpusTitle + title[0] + body[0] + corpusEnd)

        urls = hxs.xpath('//a/@href').extract()

        for url in urls:
            if(url not in self.URLS):
                if(self.COUNT < self.MAX):
                    self.URLS.append(url)
                    self.COUNT += 1

        for url in self.URLS:
            yield response.follow(url, self.parse)
