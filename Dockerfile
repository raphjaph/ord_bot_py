FROM python:3.10
# FROM nixos/nix

# RUN nix-channel --update

# RUN nix-build -A python310Full '<nixpkgs>'

WORKDIR /ord_bot

COPY . .

# ENV NIXPKGS_ALLOW_UNFREE=1

# TODO: make a shell.nix
# RUN nix-env -iA nixpkgs.google-chrome
# RUN nix-env -iA nixpkgs.chromedriver
# RUN nix-env -iA nixpkgs.python310Full
# RUN nix-env -iA nixpkgs.python310Packages.pip

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt install ./google-chrome-stable_current_amd64.deb

RUN pip install --upgrade setuptools pip

RUN pip install feedparser tweepy selenium

CMD [ "python", "-u", "ord_bot.py" ]
