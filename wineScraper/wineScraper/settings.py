# Scrapy settings for courseScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#



BOT_NAME = 'wineScraper'

SPIDER_MODULES = ['wineScraper.spiders']
NEWSPIDER_MODULE = 'wineScraper.spiders'
ITEM_PIPELINES = {
    'wineScraper.pipelines.WineScraperPipeline': 100,
}
LOG_LEVEL = 'INFO'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'courseScraper (+http://www.yourdomain.com)'
