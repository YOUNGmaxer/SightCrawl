# 爬虫项目

语言: `python`

框架: `scrapy`

## 介绍

### 结构

* `/proxy_pool_origin`

  这个目录主要是无框架的代理池程序。

* `/sights`

  这个目录是基于 `scrapy` 的核心爬虫代码。

## 测试

**运行测试**:

* `python3 -m unittest -v filepath`

* 直接运行

  ```python
  if __name__ == '__main__':
    unittest.main()
  ```

**命名**:

`test_xxx.py`

## 后续

由于将两个相对独立的项目放在一个目录下后面发现越来越不方便管理。至此这个项目的基本功能开发完成，后续将分开管理，方便部署等操作。
