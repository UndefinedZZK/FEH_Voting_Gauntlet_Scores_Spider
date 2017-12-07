#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from FEH_Voting_Gauntlet_Scores_Spider.spiders import feh_voting_gauntlet_scores_spider
from FEH_Voting_Gauntlet_Scores_Spider import settings as my_settings
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from twisted.internet import reactor
from twisted.internet import task
import json
import smtplib

Chinese_name_dict = {
	'Takumi': '拓海',
	'Hinoka': '日乃香',
	'Karel': '卡烈尔',
	'Soren': '塞内利奥',
	'Shanna': '夏娜',
	'Amelia': '艾米莉亚',
	'Katarina': '卡特琳娜',
	'Ryoma': '龙马',
    'Faye': '艾菲',
    'Rhajat': '夏拉',
    'Sigurd': '辛格尔德',
    'Catria': '卡秋娅',
    'Tharja': '萨莉亚',
    'Dorcas': '多尔卡斯',
    'Katarina': '卡特琳娜',
    'Priscilla': '普莉希拉'

}
who_is_behind = ''

crawler_settings = Settings()
crawler_settings.setmodule(my_settings)
spider_timeout = 60

gmail_user = 'fireemblemheroes.sup@gmail.com'
gmail_password = ''

sent_from = gmail_user
to = {
    'Faye': ['7612934@gmail.com'],
    'Rhajat': ['7612934@gmail.com'],
    'Sigurd': ['undefinedzzk@gmail.com'],
    'Catria': ['undefinedzzk@163.com'],
    'Tharja': ['18868102016@163.com'],
    'Dorcas': ['zekunzhou@foxmail.com'],
    'Katarina': [],
    'Priscilla': ['1227061027@qq.com']
}
subject = 'FEH情报更新'

def send_email_using_gmail(sent_from, to, subject, body):
    try:
        global gmail_user
        global gmail_password
        email_text = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (sent_from, ", ".join(to), subject, body)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print 'Email sent!'
    except:
        print 'Something went wrong...'

# Read scores json file which is generated by spider, and return a dictionary
def read_scores_json():
    score_file = open('feh_voting_gauntlet_scores.json', 'r')
    scores = json.loads(score_file.read())
    score_file.close()
    return scores

# Compare the current scores and original scores, if there are changes then append to a list
def score_changes(scores_new):
    score_change_list = []
    for key, value in scores_new.iteritems():
        print key, value['is_behind'], value['score']
        if (key not in scores_original or scores_original[key]['score'] != value['score']) and value['is_behind'] == True:
            # score_change_list.append(Chinese_name_dict[key])
            score_change_list.append(key)
        scores_original[key] = value
    return score_change_list

def update_who_is_behind(score_change_list):
    if score_change_list:
        global who_is_behind
        initial_update = who_is_behind == ''
        who_is_behind = ' '.join(score_change_list) + ' 劣势啦！'
        if initial_update is not True:
            global sent_from
            global to
            global subject
            for hero_name in score_change_list:
                email_body = ''.join(['您在FEH投票战选择的', Chinese_name_dict[hero_name], '劣势啦!'])
                if to[hero_name]:
                    send_email_using_gmail(sent_from, to[hero_name], subject, email_body)

# Very messy spider, need to refactor in the future
def run_spider():
    update_who_is_behind(score_changes(read_scores_json()))
    loop_call.stop()
    runner = CrawlerRunner(crawler_settings)
    process = runner.crawl(feh_voting_gauntlet_scores_spider.FehVotingGauntletScoresSpider)
    process.addBoth(lambda _: loop_call.start(spider_timeout, False))

# Main
print "FEH voting gaunliet score spider started!"

scores_original = {}
update_who_is_behind(score_changes(read_scores_json()))

loop_call = task.LoopingCall(run_spider)
loop_call.start(spider_timeout)

reactor.run()
