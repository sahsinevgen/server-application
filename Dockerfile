
FROM python:3.9-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./src/*.py ./src/

WORKDIR /app/src

# EXPOSE 5000

CMD [ "python3", "app.py" ]
