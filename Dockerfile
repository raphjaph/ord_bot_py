FROM python:3.10

WORKDIR /ord_bot

COPY ./ord_bot/* .

COPY . .

RUN pip install --upgrade setuptools pip

RUN pip install pipenv

CMD [ "pipenv", "run", "python", "-u", "ord_bot.py" ]
