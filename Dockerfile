FROM python:3

WORKDIR /ord_bot

COPY ./ord_bot/ .

RUN pip install tweepy feedparser

CMD [ "python", "./ord_bot.py" ]
