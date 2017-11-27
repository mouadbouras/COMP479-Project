import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import io
import re
import html2text
import os

class Spyder(scrapy.Spider):
    name = "Spyder"
    start_urls = ["http://csu.qc.ca/content/student-groups-associations"]

    def __init__(self, crawlmax=20, docID=1, corpusID=1, corpusmax=10, bytelimit=100000):
        self.BYTELIMIT = int(bytelimit)
        self.COUNT = 0;
        self.MAX = int(crawlmax)
        self.ID = int(docID)
        self.CORPUS = int(corpusID)
        self.CORPUSMAX = int(corpusmax)
        self.URLS = [
            "http://cufa.net/",
            "http://www.cupfa.org/",
            "http://www.concordia.ca/artsci/students/associations.html"
        ]

        dispatcher.connect(self.spider_closed, signals.spider_closed)

# This is the method that gets called and automatically run with scrapy
    def parse(self, response):
        h = html2text.HTML2Text()
        hxs = Selector(response)
        title = hxs.xpath('//title').extract()
        body = hxs.xpath('//body').extract()
        title[0] = h.handle(title[0])
        title[0] = title[0].strip("\r\n")

        # These checks are here because if a page has a 404 or "Page not found" in the title which is concordia.ca's 404 page
        # (but returns a 200 code) we want to increase the max because those sites won't get crawled.
        if(response.status != 200):
            self.MAX += 1
            return
        if(title[0] == "Page not found"):
            self.MAX += 1

        if(title[0] != "Page not found"):
            if(self.CORPUS < self.CORPUSMAX):
                fileName = "../Dumps/"+str(self.CORPUS) + ".txt"
                if(os.path.exists(fileName)):
                    filesize = os.stat(fileName).st_size
                    if(filesize > self.BYTELIMIT):
                        with io.open(fileName, "a", encoding="utf-8") as f:
                            f.write("</documents>")
                        if(self.CORPUS < self.CORPUSMAX):
                            self.CORPUS += 1
                        else:
                            return
                        fileName = "../Dumps/"+str(self.CORPUS) + ".txt"
                        with io.open(fileName, "a", encoding="utf-8") as f:
                            f.write("<documents>")
                        fileSize = 0
                else:
                    with io.open(fileName, "a", encoding="utf-8") as f:
                        f.write("<documents>")
                    filesize = 0

                # noHTMLRegex = re.compile('(<.*?>)|<.*?>.*?</script>|<.*?>.*?</style>|&.*?;|<.*?>.*?</iframe>|<!--.*?-->')
                # body[0] = re.sub(noHTMLRegex, ' ', body[0])
                # title[0] = re.sub(noHTMLRegex, ' ', title[0])

                h.ignore_links = True
                body[0] = h.handle(body[0])

                extracted = title[0] + '\n' + body[0]

                corpusTitle = '<document id="' + str(self.ID) + '" url= "' + response.url + '">'
                self.ID += 1
                corpusEnd = "</document>"

                with io.open(fileName, "a", encoding="utf-8") as f:
                    f.write(corpusTitle + title[0] + body[0] + corpusEnd)

                urls = hxs.xpath('//a/@href').extract()

                for url in urls:
                    if(url not in self.URLS):
                        if(len(self.URLS) < self.MAX):
                            if("http" not in url and "mailto" not in url):
                                url = response.url + url
                                if("concordia.ca" in url or "cufa.net" in url or "cupfa.org" in url):
                                    self.URLS.append(url)

                for url in self.URLS:
                    yield response.follow(url, self.parse)

    def spider_closed(self, spider):
        fileName = "../Dumps/"+str(self.CORPUS) + ".txt"
        with io.open(fileName, "a", encoding="utf-8") as f:
            f.write("</documents>")
