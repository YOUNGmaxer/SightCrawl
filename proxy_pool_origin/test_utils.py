from utils import PageGetter
import json

URL = 'http://www.66ip.cn/1.html'
URL2 = 'http://www.66ip.cn/2.html'
pageGetter = PageGetter()
res = pageGetter.get_page(URL)
res = pageGetter.get_page(URL2)
print(res)
