# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class ZhilianspiderPipeline(object):
    def __init__(self):
        self.conn = sqlite3.connect('./../zhilian.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            "create table IF NOT EXISTS infos(id integer primary key autoincrement, job_title text,job_salary text,job_address text,job_nature text,job_experience text,job_education text,job_num_people text,job_content text);")
        self.conn.commit()
    def process_item(self, item, spider):

        self.cur.execute('insert into infos(job_title,job_salary,job_address,job_nature,job_experience,job_education,job_num_people,job_content) values (?,?,?,?,?,?,?,?)',[item['job_title'],item['job_salary'],item['job_address'],item['job_nature'],item['job_experience'],item['job_education'],item['job_num_people'],item['job_content']])
        self.conn.commit()
        return item
