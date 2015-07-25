FROM pypy:latest

RUN  cd /tmp && curl -O https://bootstrap.pypa.io/get-pip.py && \
     pypy3 /tmp/get-pip.py

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/

RUN pypy3 -m pip install -r requirements.txt

COPY . /app

CMD ["pypy3", "worker.py"]
