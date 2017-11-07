# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class FehVotingGauntletScoresSpiderPipeline(object):
    def open_spider(self, spider):
        self.score_file = open('feh_voting_gauntlet_scores.json', 'w')
        self.score_and_is_Behind = {}

    def close_spider(self, spider):
    	self.score_file.write(json.dumps(self.score_and_is_Behind))
        self.score_file.close()

    def process_item(self, item, spider):
    	self.score_and_is_Behind[item['name']] = {'score': item['score'], 'is_behind': item['behind']}
        return item
