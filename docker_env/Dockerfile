# 构建可用于整个项目运行的定制环境镜像
FROM python:3.7-slim
COPY requirements.txt /usr/require/
COPY scrapyd.conf /etc/scrapyd/
WORKDIR /usr/require
RUN apt-get update && apt-get install -y gcc unixodbc-dev
RUN pip3 install --default-timeout=200 -r requirements.txt
CMD /bin/bash
