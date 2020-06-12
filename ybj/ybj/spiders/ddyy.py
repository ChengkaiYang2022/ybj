# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest

from ybj.items import YbjItem
from ybj.settings import PAGE


class DdyySpider(scrapy.Spider):
    name = 'ddyy'
    # allowed_domains = ['ddy.ema']

    def start_requests(self):
        # start_urls = ['http://fw.ybj.beijing.gov.cn/ddyy/ddyy/list']

        yield Request(
                    url='http://fw.ybj.beijing.gov.cn/ddyy/ddyy/list',
                    cb_kwargs={"page": 1},
                    callback=self.parse
        )

    def parse(self, response, **kwargs):

        for line in response.xpath("//div[@class='list']//tr"):
            re = line.xpath("td/text()").extract()
            if re:
                yield Request(
                    cb_kwargs={
                        'id': re[0],
                        'name': re[1]
                    },
                    url=PAGE.format(re[0]),
                    callback=self.parse_page
                )

        if response.request.cb_kwargs["page"] < 200:
            yield FormRequest(
                url="http://fw.ybj.beijing.gov.cn/ddyy/ddyy/list",
                # search_LIKE_yymc=&page=6&sortType=
                formdata={"search_LIKE_yymc": "",
                          "page": str(response.request.cb_kwargs["page"]+1),
                          "sortType": ""},
                cb_kwargs={"page": response.request.cb_kwargs["page"]+1},

                method="POST",
                callback=self.parse
            )

    def parse_page(self, response, **kwargs):
        d = dict()
        item = YbjItem()
        for line in response.xpath("//tr"):
            d[line.xpath('th/text()').extract_first()] = line.xpath('td/text()').extract_first()
        item['name'] = d.get('【医院名称】')
        item['code'] = d.get('【医院编码】')
        item['area'] = d.get('【所属区县】')
        item['type'] = d.get('【医院类别】') 
        item['level'] = d.get('【医院等级】')
        item['address'] = d.get('【单位地址】')
        item['postcode'] = d.get('【邮 编】')
        item['brief_info'] = d.get('【医院简介】')
        item['link'] = response.url
        yield item
        pass
