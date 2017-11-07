from FEH_Voting_Gauntlet_Scores_Spider.spiders import feh_voting_gauntlet_scores_spider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

for i in range(0, 10):
	process.crawl(feh_voting_gauntlet_scores_spider.FehVotingGauntletScoresSpider)
	process.start()