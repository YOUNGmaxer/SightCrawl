# 基础镜像信息
FROM python:3.7-slim
# 设置环境变量，即添加路径 /usr/local/bin
ENV PATH=/usr/local/bin:$PATH
# 复制依赖文件构建环境
COPY requirements.txt /usr/require/
# 指定工作目录为依赖文件目录
WORKDIR /usr/require
# 执行命令来做一些环境准备工作
RUN apt-get update && apt-get install -y gcc unixodbc-dev
RUN pip3 install --default-timeout=200 -r requirements.txt
