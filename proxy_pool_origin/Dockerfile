# 基础镜像信息
FROM python:3.7-slim
# 设置环境变量，即添加路径 /usr/local/bin
ENV PATH=/usr/local/bin:$PATH
# 将本地的代码放置到指定的镜像目录中
ADD . /code
# 指定工作目录
WORKDIR /code
EXPOSE 5000
# 执行命令来做一些环境准备工作
RUN apt-get update && apt-get install -y gcc unixodbc-dev
RUN pip3 install --default-timeout=200 -r requirements.txt
# 容器启动命令，在容器运行时，此命令会被执行
CMD python3 proxy_api.py
