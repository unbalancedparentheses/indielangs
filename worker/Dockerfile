FROM pypy:latest

RUN  cd /tmp && curl -O https://bootstrap.pypa.io/get-pip.py && \
     pypy3 /tmp/get-pip.py

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pypy3 setup.py install

CMD ["indielangs"]
