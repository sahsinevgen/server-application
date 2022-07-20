# syntax=docker/dockerfile:1
FROM python:3.9-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY app.py /app

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

