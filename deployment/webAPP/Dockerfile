FROM python:2.7-slim

WORKDIR /app

ADD . /app


RUN pip install --trusted-host pypi.python.org -r requirements.txt --proxy='https://135.251.33.16:80'

EXPOSE 80

ENV http_proxy http://135.251.33.16:80
ENV https_proxy https://135.251.33.16:80

ENV NAME World

CMD ["python","app.py"]
