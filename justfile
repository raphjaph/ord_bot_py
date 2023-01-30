default:
  just --list

all: forbid fmt

deploy2:
  ssh 8el "mkdir -p ~/infrastructure/ord_bot"
  scp -r bin/deploy bin/ord_bot.service ord_bot/*.py 8el:~/infrastructure/ord_bot
  ssh 8el "cd ~/infrastructure/ord_bot \
    && ./deploy"

deploy:
  ssh 8el "mkdir -p ~/infrastructure/ord_bot"
  scp -r Dockerfile Pipfile* ord_bot/*.py 8el:~/infrastructure/ord_bot
  ssh 8el "cd ~/infrastructure/ord_bot \
    && docker build -t ord_bot . \
    && docker stop ord_bot \
    && docker rm ord_bot \
    && docker run --name=ord_bot --restart=unless-stopped -d ord_bot"

env:
  pipenv shell --dev

forbid:
  ./bin/forbid

fmt:
  pipenv run isort . && pipenv run yapf --in-place --recursive **/*.py

install *pkg:
  pipenv install {{pkg}} --skip-lock

install-editable:
  pipenv install -e .

lock:
  pipenv lock --pre

run:
  pipenv run python ord_bot/ord_bot.py

test:
  pipenv run python -m unittest tests/*.py
