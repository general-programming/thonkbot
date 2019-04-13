FROM python:3.6-alpine

WORKDIR /app
VOLUME /app

RUN mkdir /extra
COPY requirements.txt /extra

RUN pip install -r /extra/requirements.txt

CMD ["python", "bot.py"]
