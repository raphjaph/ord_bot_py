default:
  just --list

all: forbid fmt-check

deploy:
  ssh 8el "mkdir -p ~/infrastructure/ord_bot"
  scp -r Dockerfile ord_bot/*.py 8el:~/infrastructure/ord_bot
  ssh 8el "cd ~/infrastructure/ord_bot \
    && docker build -t ord_bot . \
    && docker stop ord_bot \
    && docker rm ord_bot \
    && docker run --name=ord_bot --restart=unless-stopped -d ord_bot"

env:
  pipenv shell

forbid:
  ./bin/forbid

fmt:
  isort . && yapf --in-place --recursive **/*.py

fmt-check:
  isort -c . && yapf --diff --recursive .

install *pkg:
  pipenv install {{pkg}} --skip-lock

install-editable:
  pipenv install -e .

lock:
  pipenv lock --pre

run:
  python3 ord_bot/ord_bot.py
