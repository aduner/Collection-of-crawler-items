from selenium import webdriver
import time
driver = webdriver.Chrome()
urls = []
for page in range(1,34):
    url = f'https://job.bytedance.com/society/position?keywords=%E7%94%B5%E5%95%86&category=&location=&project=&type=&job_hot_flag=&current={page}&limit=10'
    driver.get(url)
    time.sleep(0.5)
    a = driver.find_elements_by_xpath('//div[@class="listItems__1q9i5"]/a')
    for i in a:
        urls.append(i.get_attribute("href").split('/')[-1])

with open('urls.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(urls))
