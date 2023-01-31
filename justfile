default:
  just --list

all: forbid fmt

deploy:
  ssh ordbot "mkdir -p /var/lib/ord_bot"
  scp -r Pipfile* ord_bot/*.py bin/* ordbot:/var/lib/ord_bot
  ssh ordbot "cd /var/lib/ord_bot && ./deploy"

stop:
  ssh ordbot "systemctl stop ord_bot"

env:
  pipenv shell

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
