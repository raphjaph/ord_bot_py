FROM python:3.10

WORKDIR /ord_bot

COPY . .

RUN apt-get update -y && apt-get upgrade -y
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb && apt-get install -fy

RUN wget https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver 
RUN chown root:root /usr/bin/chromedriver 
RUN chmod +x /usr/bin/chromedriver
ENV DISPLAY=:99

RUN pip install --upgrade setuptools pip
RUN pip install feedparser tweepy selenium chromedriver-binary

CMD [ "python", "-u", "ord_bot.py" ]
