# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CameraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    camera_name = scrapy.Field()
    announced = scrapy.Field()
    dp_score = scrapy.Field()
    reviewed_date = scrapy.Field()
    price_low = scrapy.Field()
    price_high = scrapy.Field()
    user_score = scrapy.Field()
    user_review_count = scrapy.Field()
    questions = scrapy.Field()
    n_own = scrapy.Field()
    n_want = scrapy.Field()
    n_had = scrapy.Field()
    # spec = scrapy.Field()
    body_type = scrapy.Field()
    sensor_size = scrapy.Field()
    
