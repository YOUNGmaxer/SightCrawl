from multiprocessing import Process
from proxy_api import app
from getter import Getter
from tester import Tester
import time

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLE = True
GETTER_ENABLE = True
API_ENABLE = True
API_HOST = 'localhost'
API_PORT = '5000'

class Scheduler():
  def schedule_tester(self, cycle=TESTER_CYCLE):
    '''
    定时测试代理
    :param cycle: 定时时长
    '''
    tester = Tester()
    while True:
      print('测试器开始运行')
      tester.run()
      time.sleep(cycle)
  
  def schedule_getter(self, cycle=GETTER_CYCLE):
    '''
    定时获取代理
    :param cycle: 定时时长
    '''
    getter = Getter()
    while True:
      print('开始抓取代理')
      getter.run()
      time.sleep(cycle)

  def schedule_api(self):
    '''
    开启 API
    '''
    app.run(API_HOST, API_PORT)
  
  def run(self):
    print('代理池开始运行')
    # 对应新建一个 Process 进程，调用 start() 运行

    # 代理池测试模块运行
    if TESTER_ENABLE:
      tester_process = Process(target=self.schedule_tester)
      tester_process.start()

    # 代理捕获模块运行
    if GETTER_ENABLE:
      getter_process = Process(target=self.schedule_getter)
      getter_process.start()

    # api模块运行
    if API_ENABLE:
      api_process = Process(target=self.schedule_api)
      api_process.start()

scheduler = Scheduler()
scheduler.run()
