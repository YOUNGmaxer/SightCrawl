FROM python:3.7
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip3 install --default-timeout=100 -r requirements.txt
CMD python3 proxy_api.py
