import scrapy

class FehVotingGauntletScoresSpider(scrapy.Spider):
    name = "feh_voting_gauntlet_scores"
    start_urls = [
        'https://support.fire-emblem-heroes.com/voting_gauntlet/tournaments/8',
    ]

    def parse(self, response):
        for tournaments in response.xpath("//p[@class='name']/../../.."):
            yield {
                'name': str(tournaments.xpath("./div/div/p/text()").extract_first()),
                'score': str(tournaments.xpath("./div/div/p[not(@*)]/text()").extract_first()),
                'behind': tournaments.xpath("@class").extract_first()[-6:] == 'behind',
            }