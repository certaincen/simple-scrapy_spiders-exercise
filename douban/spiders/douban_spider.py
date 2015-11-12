#! -*- coding:utf=8 -*-
import scrapy
from douban.items import DoubanItem
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
import json

class DoubanSpider(scrapy.spiders.Spider):
    name = "douban"
    allowed_domains = ['douban.com']
    sta_url = "http://www.douban.com/tag/%E9%99%88%E6%84%8F%E6%B6%B5/"
    start_urls = [sta_url]


    def save_json(self, item):
        save_dict = {}
        save_dict['category'] = item['category']
        save_dict['title'] = item['title']
        save_dict['desc'] = item['desc']
        with open('douban.json', 'a') as fout:
            json.dump(save_dict, fout, encoding="utf-8")


    def movie_parse(self, response):
        xpath_url = "//div[contains(@class,'mod ')]"
        xpath_link = "//div[@class='paginator']"
        base_url = get_base_url(response)
        flag = True
        for sel in response.xpath(xpath_url):
            s =  sel.xpath('.//a[@class="title"]/text()').extract()
            print "content is" + str(s)
            if not s:
                flag = False
                break
            item = DoubanItem()
            item['category'] = sel.xpath('./@class').extract()[0][4:-5]
            item['title'] = sel.xpath('.//a[@class="title"]/text()').extract()
            item['desc'] = sel.xpath('.//div[@class="desc"]/text()').extract()
            yield item
#            self.save_json(item)
        url = response.xpath(xpath_link).xpath('.//span[@class="next"]').xpath('./a/@href').extract()[0]
        if flag:
            print "current href is " + str(url)
            print "next url is " + urljoin_rfc(base_url, url)
            yield scrapy.Request(urljoin_rfc(base_url, url), callback=self.movie_parse)




    def parse(self, response):
        for url in response.xpath("//a[@class='more-links']/@href").extract()[0:2]:
            yield scrapy.Request(url, callback=self.movie_parse)
    #    xpath_url = "//div[@class='clearfix mod']"
    #    for sel in response.xpath(xpath_url):
    #        item = DoubanItem()
    #        div_content = sel.xpath('.//div[contains(@id, "")]')
    #        item['category'] = div_content.xpath('./@id').extract()
    #        item['title'] = div_content.xpath('.//a[@class="title"]/text()').extract()
    #        item['desc'] = div_content.xpath('.//div[@class="desc"]/text()').extract()
    #        yield item
