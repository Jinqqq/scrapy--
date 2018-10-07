# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import lxml.html
from ZhiLianSpider.items import ZhilianspiderItem
import time
import sqlite3

class JobProfile:
    """
    工作描述类，模型类，对数据进行清洗
    """
    def __init__(self):
        self.job_url = ""

    #限制薪资待遇范围
    def salary_limit(self):
        return True

    #限制地区
    def area_limit(self):
        return True

    # 数据条数判断
    @staticmethod
    def data_num_judge(url_str):
        # https: // sou.zhaopin.com /?p = 3 & pageSize = 60 & jl = 489 & kw = python & kt = 3
        page1 = int(url_str.split('p=')[1].split('&')[0])
        conn = sqlite3.connect('./../zhilian.db')
        cur = conn.cursor()
        infos = cur.execute('select * from infos')
        page2 = infos.fetchall()
        if (page1 - 2) * 60 <= len(page2):
            return False
        else:
            return True


class ZhilianSpiderSpider(scrapy.Spider):
    name = 'zhilian_spider'
    # allowed_domains = ['baidu.com']
    # start_urls = ['https://sou.zhaopin.com/?pageSize=60&jl=489&kw=python&kt=3']





    def start_requests(self):
        url_str = "https://sou.zhaopin.com/?pageSize=60&jl=489&kw=python&kt=3"
        yield Request(url=url_str,callback=self.parse,meta={"page":"3"})

    def parse(self, response):
        url_response = response.url
        print("url_response:::::::::::::::::::::::::::::",url_response)
        job_urls = []
        job_urls = response.xpath('//div[@class="jobName"]/a/@href').extract()
        job_urls.append(url_response)
        print("job_urls[-1]:::::::::::::::::::::::::::::::::",job_urls[-1])
        for job_url in job_urls:
            print("job_url::::::",job_url)
            if job_url == url_response:
                job_profile = JobProfile()
                while job_profile.data_num_judge(job_url):
                    time.sleep(3)
                yield Request(url=url_response,callback=self.parse, meta={"page":"3"})
            else:
                yield Request(url=job_url,callback=self.job_info,meta={"page":"0"},dont_filter=True)


    def job_info(self,response):

        # 标题
        try:
            job_title = response.css("div.fl h1::text").extract()[0]
        except:
            job_title = 'none'
        # 工资
        try:
            job_salary = response.xpath('//div[@class="terminalpage-left"]/ul/li[1]/strong/text()').extract()[0]
        except:
            job_salary = 'none'
        # 地点
        try:
            job_address = response.xpath('//div[@class="terminalpage-left"]/ul/li[2]/strong/a/text()').extract()[0]
        except:
            job_address = 'none'
        # 工作性质
        try:
            job_nature = response.xpath('//div[@class="terminalpage-left"]/ul/li[4]/strong/text()').extract()[0]
        except:
            job_nature = 'none'
        # 工作经验
        try:
            job_experience = response.xpath('//div[@class="terminalpage-left"]/ul/li[5]/strong/text()').extract()[0]
        except:
            job_experience = 'none'
        # 最低学历
        try:
            job_education = response.xpath('//div[@class="terminalpage-left"]/ul/li[6]/strong/text()').extract()[0]
        except:
            job_education = 'none'
        # 招聘人数
        try:
            job_num_people = response.xpath('//div[@class="terminalpage-left"]/ul/li[7]/strong/text()').extract()[0]
        except:
            job_num_people = 'none'
        # 内容
        contents1 = response.xpath('//div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/p/text()').extract()
        contents2 = response.css('div.tab-cont-box div.tab-inner-cont div::text').extract()
        contents3 = response.xpath('//div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/p/span/text()').extract()
        contents4 = response.xpath('//div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/div/div/p/span/span/text()').extract()
        contents5 = response.xpath('//div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/div/p/text()').extract()
        contents_str = ''
        for i in contents1:
            contents_str += i
        for i in contents2:
            contents_str += i
        for i in contents3:
            contents_str += i
        for i in contents4:
            contents_str += i
        for i in contents5:
            contents_str += i
        job_content = ' '.join(contents_str.split())

        job_item = ZhilianspiderItem()
        job_item['job_title'] = job_title
        job_item['job_salary'] = job_salary
        job_item['job_address'] = job_address
        job_item['job_nature'] = job_nature
        job_item['job_experience'] = job_experience
        job_item['job_education'] = job_education
        job_item['job_num_people'] = job_num_people
        job_item['job_content'] = job_content

        yield job_item




