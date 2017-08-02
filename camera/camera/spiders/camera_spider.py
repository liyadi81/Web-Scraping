import scrapy
from camera.items import CameraItem

class CameraSpider(scrapy.Spider):
    name = "camera_spider"
    allowed_urls = ['https://www.dpreview.com/']
    start_urls = ['https://www.dpreview.com/products/cameras/all']
    
    def verify(self, content):
        if isinstance(content, list):
            if len(content) > 0:
                return content[0]
            else:
                return ""
        else:
            return content    
            
    def parse(self, response):
        cameralist = response.xpath('//*[@id="combinedProductList"]/div/table//tr[re:test(@class, "product.*")]/td[re:test(@class, "product.*")]')
        urls = cameralist.xpath('.//div[@class="name"]/a/@href').extract()
        
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_each)
    
    
    def parse_each(self, response):
        item = CameraItem()
        
        camera_name = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        
        announced = None
        if len(response.xpath('//div[@class="shortSpecs"]/text()').extract()) >= 2:
            announced = response.xpath('//div[@class="shortSpecs"]/text()').extract()[1].strip()
        
        dp_score = response.xpath('//div[@class="award"]//span[@class="value"]/text()').extract_first()
        
        reviewed_date = None
        if response.xpath('//div[@itemprop="datePublished"]/text()').extract_first() != None:
            reviewed_date = response.xpath('//div[@itemprop="datePublished"]/text()').extract_first().strip()
            
        price_low = None
        price_high = None
        if response.xpath('//div[@class="price range"]/span/text()').extract_first() != None:
            price_low = response.xpath('//div[@class="price range"]/span/text()').extract()[0]
        if len(response.xpath('//div[@class="price range"]/span/text()').extract()) >= 3:
            price_high = response.xpath('//div[@class="price range"]/span/text()').extract()[2]
        
        user_score = response.xpath('//div[@class="score"]//meta[@itemprop="ratingValue"]/@content').extract_first()
        user_review_count = response.xpath('//div[@class="score"]//span[@itemprop="reviewCount"]/text()').extract_first()
        questions = response.xpath('//div[@class="item questionsAndAnswers"]/div[2]/div[1]/text()').extract_first()
        
        n_own = None
        n_want = None
        n_had = None
        if response.xpath('//div[@class="item gearList"]//td/text()').extract_first() != None:
            n_own = response.xpath('//div[@class="item gearList"]//td/text()').extract()[0]
        if len(response.xpath('//div[@class="item gearList"]//td/text()').extract()) >= 2:
            n_want = response.xpath('//div[@class="item gearList"]//td/text()').extract()[1]
        if len(response.xpath('//div[@class="item gearList"]//td/text()').extract()) >= 3:
            n_had = response.xpath('//div[@class="item gearList"]//td/text()').extract()[2]
        
        # spec_list = response.xpath('//div[@class="rightColumn quickSpecs"]/table//tr')
        # spec = []
        # for row in spec_list:
            # spec_name = row.xpath('./td[@class="label"]/text()').extract_first()
            # spec_value = row.xpath('./td[@class="value"]/text()').extract_first()
            # spec.append(spec_name)
            # spec.append(spec_value)
            # spec.append(';')
        specs = response.xpath('//div[@class="rightColumn quickSpecs"]/table//tr')
        
        camera_name = self.verify(camera_name)
        announced = self.verify(announced)
        dp_score = self.verify(dp_score)
        reviewed_date = self.verify(reviewed_date)
        price_low = self.verify(price_low)
        price_high = self.verify(price_high)
        user_score = self.verify(user_score)
        user_review_count = self.verify(user_review_count)
        questions = self.verify(questions)
        n_own = self.verify(n_own)
        n_want = self.verify(n_want)
        n_had = self.verify(n_had)
        
        
        item['camera_name'] = camera_name
        item['announced'] = announced
        item['dp_score'] = dp_score
        item['reviewed_date'] = reviewed_date
        item['price_low'] = price_low
        item['price_high'] = price_high
        item['user_score'] = user_score
        item['user_review_count'] = user_review_count
        item['questions'] = questions
        item['n_own'] = n_own
        item['n_want'] = n_want
        item['n_had'] = n_had
        for i in specs:
            if i.xpath('./td[@class="label"]/text()').extract_first() == 'Body type':
                item['body_type'] = i.xpath('./td[@class="value"]/text()').extract_first()
            if i.xpath('./td[@class="label"]/text()').extract_first() == 'Sensor size':
                item['sensor_size'] = i.xpath('./td[@class="value"]/text()').extract_first()
        
        yield item
        