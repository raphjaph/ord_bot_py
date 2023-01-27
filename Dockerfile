FROM python:3

WORKDIR /ord_bot

COPY . .

RUN pip install tweepy feedparser

CMD [ "python", "./ord_bot.py" ]
