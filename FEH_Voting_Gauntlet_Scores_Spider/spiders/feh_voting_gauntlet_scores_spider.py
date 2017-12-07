import scrapy

class FehVotingGauntletScoresSpider(scrapy.Spider):
    name = "feh_voting_gauntlet_scores"
    start_urls = [
        'https://support.fire-emblem-heroes.com/voting_gauntlet/tournaments/9',
    ]

    def parse(self, response):
        tournaments_list = response.xpath("//p[@class='name']/../../..")
        if len(tournaments_list) == 15:
            tournaments_list = tournaments_list[:1]
        elif len(tournaments_list) == 14:
            tournaments_list = tournaments_list[:2]
        elif len(tournaments_list) == 12:
            tournaments_list = tournaments_list[:4]
        else:
            pass
        for tournaments in tournaments_list:
            yield {
                'name': str(tournaments.xpath("./div/div/p/text()").extract_first()),
                'score': str(tournaments.xpath("./div/div/p[not(@*)]/text()").extract_first()),
                'behind': tournaments.xpath("@class").extract_first()[-6:] == 'behind',
            }