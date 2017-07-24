from scrapy import Spider
from camera.items import CameraItem

class CameraSpider(Spider):
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
        rows = response.xpath('//*[@id="combinedProductList"]/div/table//tr[re:test(@class, "product.*")]/td')
        for i in range(1, len(rows)):
            cameraname = row[i].xpath('./div[2]/div[1]/a/text()').extract_first()
            pixels = row.xpath('./div[2]/div[3]/div/text()').extract()[0].strip()
            screen = row.xpath('./div[2]/div[3]/div/text()').extract()[1].split('| ')[1]
            sensortype = row.xpath('./div[2]/div[3]/div/text()').extract()[2].split('| ')[1]
            time = row.xpath('./div[2]/div[2]/text()').extract()
            price = row.xpath('./div[2]/div[4]/a/text()').extract()
            
            cameraname = self.verify(cameraname)
            pixels = self.verify(pixels)
            screen = self.verify(screen)
            sensortype = self.verify(sensortype)
            time = self.verify(time)
            price = self.verify(price)
            
            item = CameraItem()
            item['cameraname'] = cameraname
            item['pixels'] = pixels
            item['screen'] = screen
            item['sensortype'] = sensortype
            item['time'] = time
            item['price'] = price
            yield item
            