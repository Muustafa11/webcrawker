# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

#import scrapy


#class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    pass


import scrapy

class AmazonItem(scrapy.Item):
    brand_name = scrapy.Field()
    brief = scrapy.Field()
    price = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()

