import requests
from selenium import webdriver
# By是一个类，属性表示使用哪种元素定位方式
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
# 用于让 WebDriver 等待，满足一定条件之后才执行
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
URL_SELECTED = ['66ip']
REQUIRED_COOKIE_NAME = '_ydclearance'

class PageGetter():
  def __init__(self):
    self.myCookie = {}

  def get_page(self, url):
    if url.find('66ip'):
      res = requests.get(url, cookies=self.myCookie)
      if res.status_code == 200:
        print('[requests]', res.text)
        return res.text
      elif res.status_code == 521:
        try:
          # 注意这里browser如果close之后需要重新创建实例再使用，否则会报错
          # browser = webdriver.Chrome()
          browser.get(url)
          # 等到页面内容加载出来再去获取 Cookie
          wait = WebDriverWait(browser, 10)
          wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'containerbox'))
          )
          cookies = browser.get_cookies()
          for cookie in cookies:
            self.myCookie[cookie['name']] = cookie['value']
          print('cookie]', self.myCookie, type(self.myCookie))
          return browser.page_source
        finally:
          # browser.close()
          print('finally')
      else:
        print('[异常]出现其他状态码')
    else:
      res = requests.get(url)
      if res.status_code == 200:
        return res.content
      else:
        print('状态码异常:', res.status_code)
        return -1
