default:
  just --list

deploy:
  ssh 8el "mkdir -p ~/infrastructure/ord_bot"
  scp -r Dockerfile ord_bot/*.py 8el:~/infrastructure/ord_bot
  ssh 8el "cd ~/infrastructure/ord_bot \
    && docker build -t ord_bot . \
    && docker stop ord_bot \
    && docker start ord_bot"

all: forbid fmt-check

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
