import requests
from lxml import etree
from selenium import webdriver
from time import sleep
base_url = 'https://www.nytimes.com'
option = webdriver.ChromeOptions()
option.add_argument("--user-data-dir=" +
                    r"C:\\Users\\85400\\AppData\\Local\\Google\\Chrome\\User Data\\")
driver = webdriver.Chrome(chrome_options=option)
driver.get('https://www.nytimes.com/search?dropmab=false&query=Coronavirus&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=best&types=article')
sleep(5)
while True:
    sleep(0.2)
    try:
        next_button = driver.find_element_by_xpath(
            '//*[@id="site-content"]//button[contains(text(), "Show More")]')
        driver.execute_script("arguments[0].click();", next_button)
    except:
        print("到头了!")
        break
# title = driver.find_elements_by_xpath(
#     '//*[@id="site-content"]/div/div[2]/div[2]/ol/li/div/div/div/a/h4/text()')
# # urls = driver.find_elements_by_xpath(
# #     '//*[@id="site-content"]//li[@class="css-1l4w6pd"]//a/@href')
# # urls = '\n'.join([base_url+i for i in urls])
# titles = '\n'.join([i for i in title])
# # with open('newyork_url.txt', 'w', encoding='utf-8') as f:
# #     f.write(urls)
# with open('titile.txt', 'w', encoding='utf-8') as f:
#     f.write(titles)


# with open('a.txt', 'r') as f:
#     urls = f.read()
# urls = urls.split('\n')
# urls = '\n'.join([base_url+i for i in urls][:2558])
# with open('newyork_url.txt', 'w', encoding='utf-8') as f:
#     f.write(urls)
