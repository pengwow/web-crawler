# -*- coding:utf-8 -*-

import os

#os.system("scrapy crawl item_bank")
#os.system("scrapy crawl level_subjects")

# DEBUG
from scrapy import cmdline
# cmdline.execute("scrapy crawl item_bank".split())
# cmdline.execute("scrapy crawl level_subjects".split())
# cmdline.execute("scrapy crawl level_grade".split())
cmdline.execute("scrapy crawl library_chapter".split())
