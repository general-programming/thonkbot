FROM python:3.6-alpine

WORKDIR /app
VOLUME /app

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
