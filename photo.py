
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()
driver.get("https://www.flickr.com/explore/2015/05/17")

csv_file = open('photo.csv', 'a+', newline='')
writer = csv.writer(csv_file)
writer.writerow(['date', 'url'])

index = 1
while True:
    try:
        print("Scraping Page number " + str(index))
        index += 1
        
        # Scroll down to the bottom of the page
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:	
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

         # extract url for each picture
        pics = driver.find_elements_by_xpath('//div[starts-with(@class, "view photo-list-photo-view")]')
        date = driver.find_element_by_xpath('//a[@class="butt curr-date"]').text
        print("total pics on this page:" + str(len(pics)) + " date: " + date)
        print(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
        for pic in pics[:100]:
            pic_dict = {}
            url = pic.find_element_by_xpath('.//a[@class="overlay"]').get_attribute('href')
            pic_dict['date'] = date
            pic_dict['url'] = url
            writer.writerow(pic_dict.values())

        button = driver.find_element_by_xpath('//a[@class="butt page-back"]')
        button.click()
        time.sleep(4)
    
    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
        break    


# csv_file = open('photo.csv', 'w')

# writer = csv.writer(csv_file)
# writer.writerow(['date','title', 'url'])

# index = 1


# while True:
	# try:
		# print("Scraping Page number " + str(index))
		# index = index + 1

		# pics = driver.find_elements_by_xpath('//ol[@class="bv-content-list bv-content-list-Reviews bv-focusable"]/li')
		# for review in reviews:
			# review_dict = {}

			# writer.writerow(review_dict.values())

		# button = driver.find_element_by_xpath('//span[@class="bv-content-btn-pages-next"]')
		# button.click()
		# time.sleep(2)
	# except Exception as e:
		# print(e)
		# csv_file.close()
		# driver.close()
		# break


