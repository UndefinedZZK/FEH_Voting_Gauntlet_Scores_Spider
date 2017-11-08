# FEH_Voting_Gauntlet_Scores_Spider

Two way to use for now:

1. ``scrapy crawl feh_voting_gauntlet_scores``
   
   Which generate a json file of the scores. It can be used when error occurs with like ``No JSON object could be decoded``
   
2. python setup.py

   This is to execute the program. You need to scan a QR code to login your WeChat account. It is suggested that you should not use your main account since you may be restricted to loginto other WeChat platform.
