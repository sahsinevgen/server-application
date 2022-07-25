
FROM alt:p10

RUN apt-get update;\
    apt-get install -y python3\
                       python3-module-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./src/*.py ./src/

WORKDIR /app/src

EXPOSE 5000

CMD [ "python3", "app.py" ]
