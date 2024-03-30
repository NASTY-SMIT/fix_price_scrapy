import scrapy


class FixPriceScrapyItem(scrapy.Item):
    timestamp = scrapy.Field()
    RPC = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    marketing_tags = scrapy.Field()
    section = scrapy.Field()
    price_data = scrapy.Field()
    assets = scrapy.Field()
    metadata = scrapy.Field()
