# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #工作名
    job_title = scrapy.Field()
    #工资
    job_salary = scrapy.Field()
    #地点
    job_address = scrapy.Field()
    #工作性质
    job_nature = scrapy.Field()
    #工作经验
    job_experience = scrapy.Field()
    #最低学历
    job_education = scrapy.Field()
    #招聘人数
    job_num_people = scrapy.Field()
    # 工作要求
    job_content = scrapy.Field()



