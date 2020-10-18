from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
import requests
import json
import base64
from io import BytesIO
from PIL import Image
from sys import version_info
import json
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['bx_urls']
collection = db['urls_4296']


def base64_api(img, uname='账号', pwd='密码'):
    # 打码平台接口
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post(
        "http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"], result["data"]["id"]
    else:
        return result["message"], '凑数'
    return ""


def reportError(id):
    data = {"id": id}
    result = json.loads(requests.post(
        "http://api.ttshitu.com/reporterror.json", json=data).text)
    if result['success']:
        return "报错成功"
    else:
        return result["message"]
    return ""


def request_download(url):
    r = requests.get(url)
    with open('./image/verification_code.png', 'wb') as f:
        f.write(r.content)


def driver_start(url=None):
    url = 'http://xkz.cbirc.gov.cn/bx/'
    # 设置chrome浏览器无界面模式
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver = webdriver.Chrome()
    driver.set_window_size(1200, 800)
    driver.get(url)
    return driver


def verification(driver):

    def get_img(img):
        for _ in range(5):
            driver.save_screenshot('.\\image\\photo.png')
            location = img.location  # 获取验证码x,y轴坐标
            size = img.size  # 获取验证码的长宽

            # 无界面启动截图
            rangle = (int(location['x']),
                      int(location['y']),
                      int(location['x'] + size['width']),
                      int(location['y'] + size['height']))

            # 有界面截图
            # x = int(location['x'])+180
            # y = int(location['y'])+80
            # rangle = (x,
            #         y,
            #         x + int(size['width'])+25,
            #         y + int(size['height']))

            i = Image.open(".\\image\\photo.png")  # 打开截图
            frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域

            try:
                # 保存我们接下来的验证码图片 进行打码
                frame4.save(".\\image\\verification_code.png")
                return Image.open('./image/verification_code.png')
            except:
                print('验证码没有加载出来，等待10s')
                time.sleep(10)
                continue
        else:
            return Image.open('./image/a.png')

    def verify():
        # 验证验证码是否正确
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            return True
        return False

    def revalidation(v_id):
        print('验证码错误，重新验证')
        print(reportError(v_id))
        img.click()
        v_code_img = get_img(img)
        v_code, v_id = base64_api(v_code_img)
        #输入验证码
        verification_code.send_keys(v_code)
        submit.click()

        time.sleep(0.5)
        if verify():
            return driver
        else:
            return revalidation(v_id)

    verification_code = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "verificationCode")))
    img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "verifyCodeImg")))
    time.sleep(0.5)
    v_code_img = get_img(img)
    # 调用接口解析验证码
    v_code, v_id = base64_api(v_code_img)
    verification_code.send_keys(v_code)

    submit = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="show_msg"]/table/tbody/tr[3]/td/input')))
    submit.click()
    time.sleep(0.5)
    if verify():
        return driver
    else:
        return revalidation(v_id)


def if_need_verification(driver):
    # 检验是否有验证码，有的话验证
    try:
        driver.find_element_by_xpath('//*[@id="ext-gen14"]/div[1]/table')
    except NoSuchElementException:
        driver = verification(driver)


def if_load(driver):
    try:
        driver.find_element_by_xpath('//*[@id="ext-gen14"]/div[1]/table')
        return True
    except NoSuchElementException:
        print('未加载等待中！')
        return False


def select_tpye(driver):
    driver.find_element_by_id('organTypeNo').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[13]/div[1]/div[4]').click()
    driver.find_element_by_id('reportSearch').click()


def get_urls(driver):
    def save_urls(url):
        result = collection.insert({'url': url})
    urls = driver.find_elements_by_xpath(
        '//*[@id="ext-gen14"]/div/table/tbody/tr/td[5]/div/a')
    for i in urls:
        url=i.get_attribute('href')
        save_urls(url)
    return urls


driver = driver_start()
time.sleep(1)
if_need_verification(driver)
select_tpye(driver)
time.sleep(1)
if_need_verification(driver)
page=driver.find_element_by_id('ext-comp-1003')
page.send_keys(input("输入page: "))
page.send_keys(Keys.ENTER)
time.sleep(1)
for _ in range(3799,4296):
    if_need_verification(driver)
    time.sleep(0.3)
    for __ in range(10):
        if if_load(driver):
            break
        time.sleep(3)
    else:
        print('等待时间过长')
    get_urls(driver)
    next_page = driver.find_element_by_id('ext-gen36')
    print(_+1)
    try:
        next_page.click()
    except:
        time.sleep(1)
    time.sleep(0.5)
input('end?:')
driver.quit()
