FROM pypy:latest

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pypy3 setup.py install

CMD ["indielangs"]
