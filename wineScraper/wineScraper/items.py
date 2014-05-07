# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class WineItem(Item):
    # define the fields for your item here like:
    # name = Field()

    name = Field()
    reviews = Field()
    description = Field()
    price = Field()



