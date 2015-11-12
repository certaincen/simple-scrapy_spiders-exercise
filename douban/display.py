#! -*- coding:utf-8 -*-
import json

with open('./spiders/douban.json', 'r') as fin:
    item_list = json.load(fin)
    for item in item_list:
        for i in item['title']:
            print i.encode("utf-8")

