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
db = client['bx_data']
collection = db['data']


def base64_api(img, uname='user', pwd='password'):
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


def driver_start(url=None,proxy=None):
    # url = 'http://xkz.cbirc.gov.cn/bx/'
    # 设置chrome浏览器无界面模式
    chrome_options = Options()
    # if proxy:
    #     chrome_options.add_argument(f"--proxy-server={proxy}")
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver = webdriver.Chrome()
    driver.set_window_size(1200, 800)
    # driver.get(url)
    return driver


def verification(driver):

    def get_img(img, flag=False):
        for _ in range(5):
            driver.save_screenshot('.\\image\\photo.png')
            location = img.location  # 获取验证码x,y轴坐标
            size = img.size  # 获取验证码的长宽
            if flag:
                # 无界面启动截图
                rangle = (int(location['x']),
                          int(location['y']),
                          int(location['x'] + size['width']),
                          int(location['y'] + size['height']))
            else:
                # 有界面截图
                x = int(location['x'])+180
                y = int(location['y'])+80
                rangle = (x,
                          y,
                          x + int(size['width'])+25,
                          y + int(size['height']))

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

    def revalidation(v_id, num=0):
        if num > 10:
            return False
        print('验证码错误，重新验证')
        print(reportError(v_id))
        img.click()
        v_code_img = get_img(img)
        v_code, v_id = base64_api(v_code_img)
        verification_code.send_keys(v_code)

        submit.click()
        time.sleep(0.5)
        if verify():
            return driver
        else:
            return revalidation(v_id, num=num+1)

    verification_code = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "verificationCode")))
    img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "verifyCodeImg")))
    time.sleep(0.5)
    v_code_img = get_img(img)
    # 调用接口解析验证码
    v_code, v_id = base64_api(v_code_img)
    if not v_code:
        print('出现错误！！！！！！！！！！！')
        driver.quit()
    # print(f'验证码:{v_code}')
    verification_code.send_keys(v_code)

    submit = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="show_msg"]/table/tbody/tr[3]/td/input')))
    submit.click()
    time.sleep(0.5)
    if verify():
        return if_need_verification(driver)
    else:
        return revalidation(v_id)


def if_need_verification(driver):
    # 检验是否有验证码，有的话验证
    try:
        driver.find_element_by_xpath('//*[contains(text(), "机构名称")]/../td[2]')
    except NoSuchElementException:
        driver = verification(driver)


def if_load(driver):
    try:
        driver.find_element_by_xpath('//*[contains(text(), "机构名称")]')
        return True
    except NoSuchElementException:
        print('未加载等待中！')
        return False


def get_data(driver):
    def get_fields(field):
        f = driver.find_elements_by_xpath(
            f'//*[contains(text(), "{field}")]/../td[2]')
        res = []
        for i in f:
            res.append(i.text)
        if len(res) == 2:
            return res[0], res[1]
        else:
            return res[0], '暂无数据'

    def get_field(field):
        try:
            return driver.find_element_by_xpath(
                f'//*[contains(text(), "{field}")]/../td[2]').text
        except NoSuchElementException:
            return '暂无数据'

    def if_exist():
        try:
            return driver.find_element_by_xpath(
                f'//b[contains(text(), "变更前机构信息")]').text
        except NoSuchElementException:
            return False

    jg_num = get_field('机构编码')
    jg_name, bg_jg_name = get_fields('机构名称')
    address, bg_address = get_fields('机构地址')
    time_one = get_field('发证日期')
    time_two = get_field('批准成立日期')
    organ = get_field('发证机关')
    return {'jg_name': jg_name,
            'jg_num': jg_num,
            'address': address,
            'time_one': time_one,
            'time_two': time_two,
            'organ': organ,
            'bg_jg_name': bg_jg_name,
            'bg_address': bg_address}


def save_data(data):
    collection.insert_one(data)


def run(num):
    with open('4296urls.json', 'r') as f:
        urls = json.load(f)[num:]
    driver = driver_start()
    try:
        for url in urls:
            driver.get(url)
            time.sleep(1)
            if_need_verification(driver)

            for __ in range(10):
                if if_load(driver):
                    break
                time.sleep(3)
            else:
                print('等待时间过长')

            data = get_data(driver)
            data['url'] = url
            save_data(data)

            num += 1
            print(num, "    :", url)
        input('end?:')
        driver.quit()
        return False
    except:
        driver.quit()
        print("*"*40)
        print("*"*40)
        print('网络错误准备重启！！！')
        print("*"*40)
        print("*"*40)
        time.sleep(5)
        return num


if __name__ == "__main__":
    num = 1
    while num:
        num = run(num)
