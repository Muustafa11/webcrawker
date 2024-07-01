import scrapy

class AmazonItem(scrapy.Item):
    id = scrapy.Field()
    brand_name = scrapy.Field()
    brief = scrapy.Field()
    price = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()
