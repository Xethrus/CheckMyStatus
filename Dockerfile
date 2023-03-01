FROM python:3.10-slim-buster

WORKDIR /app

RUN rm -rf /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

CMD ["python", "webserver.py"]

