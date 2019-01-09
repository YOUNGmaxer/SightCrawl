from flask import Flask, g
from flask import jsonify
from redisClient import RedisClient

# 定义了导出模块时能够导出的符号
__all__ = ['app']
app = Flask(__name__)

def get_conn():
  if not hasattr(g, 'redis'):
    g.redis = RedisClient()
  return g.redis

@app.route('/')
def index():
  return '<h2>Welcome to Proxy Pool System</h2>'

@app.route('/random')
def get_proxy():
  '''
  获取随机可用代理
  :return: 随机代理
  '''
  conn = get_conn()
  return conn.random()

@app.route('/count')
def get_counts():
  '''
  获取代理池总量
  :return: 代理池总量
  '''
  conn = get_conn()
  return str(conn.count())

@app.route('/exist/<string:ip>')
def isExist(ip):
  conn = get_conn()
  successText = { 'ret': True }
  failedText = { 'ret': False }
  res = (failedText, successText)[conn.exists(ip)]
  # 返回 JSON 格式数据
  return jsonify(res)

if __name__ == '__main__':
  app.run()
