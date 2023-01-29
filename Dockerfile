# FROM zenika/alpine-chrome
# FROM python:3
FROM nixos/nix

RUN nix-channel --update

RUN nix-build -A pythonFull '<nixpkgs>'

WORKDIR /ord_bot

COPY ./ord_bot .

RUN pip install tweepy feedparser html2image pillow

CMD [ "python", "-u", "ord_bot.py" ]
