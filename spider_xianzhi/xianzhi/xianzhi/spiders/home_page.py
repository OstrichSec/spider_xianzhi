# -*- coding: utf-8 -*-
import scrapy
import re
import csv
from xianzhi.items import XianzhiItem
from lxml import etree
from html import unescape
from scrapy_redis.spiders import RedisSpider


class HomePageSpider(scrapy.Spider):
    name = 'home_page'
    allowed_domains = ['xz.aliyun.com']
    base_url = 'https://xz.aliyun.com/?page='
    cata_ur_list = []
    for i in range(1,128):
        cata_ur_list.append(base_url+str(i))
    start_urls = cata_ur_list

    def parse(self, response):
        art_list = list()
        source_of_article_list=response.xpath('/html/body/div[2]/div/div[1]/div/div/div[2]/table/tr')
        #print(source_of_article_list)
        for each in source_of_article_list:
            art_item = XianzhiItem()
            art_dict = {}
            a = each.xpath('td/p[1]/a').extract()[0]
            art_url = 'https://xz.aliyun.com/' + re.search(' href="(.*?)">\n', a, re.S).group(1)
            art_item['art_url'] = art_url
            art_item['art_name'] = re.search('\n        (.*?)</a>', a, re.S).group(1)
            art_item['author'] = each.xpath('td/p[2]/a[1]/text()').extract()[0]
            art_item['category'] = each.xpath('td/p[2]/a[2]/text()').extract()[0]
            yield scrapy.Request(art_url,headers=self.settings['HEADERS'],callback=self.parse_detail,meta={'art_item':art_item})
            #art_dict['art_url'] = 'https://xz.aliyun.com/' + re.search(' href="(.*?)">\n', a, re.S).group(1)
            #art_dict['art_name'] = re.search('\n        (.*?)</a>', a, re.S).group(1)
            #art_dict['author'] = each.xpath('td/p[2]/a[1]/text()').extract()[0]
            #art_dict['category'] = each.xpath('td/p[2]/a[2]/text()').extract()[0]
            #art_list.append(art_dict)
        #with open('/root/spider_xianzhi/output/先知文章url列表.csv','a',encoding='utf-8') as f:
            #writer = csv.DictWriter(f,fieldnames=['art_name','art_url','author','category'])
            #writer.writeheader()
            #writer.writerows(art_list)
    def parse_detail(self,response):
        art_item = response.meta['art_item']
        post_time = response.xpath('/html/body/div[2]/div/div[1]/div[1]/div/div/div[1]/div/span[1]/span[2]/text()').extract_first()
        topic_content = etree.HTML(response.xpath('//*[@id="topic_content"]').extract_first())
        body_html = unescape(etree.tostring(topic_content).decode('utf-8'))
        art_item['post_time'] = post_time
        art_item['detail'] = body_html
        yield art_item
#
