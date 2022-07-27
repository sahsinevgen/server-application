
FROM alt:p10

RUN apt-get update;\
    apt-get install -y python3\
                       python3-module-pip\
                       python3-module-SQLAlchemy\
                       python3-module-flask\
                       python3-module-flask-restx\
                       python3-module-werkzeug\
                       python3-module-psycopg2

COPY ./src/*.py /app/src/

WORKDIR /app/src

EXPOSE 5000

CMD [ "python3", "app.py" ]
