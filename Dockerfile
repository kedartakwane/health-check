FROM python:3.10.2-slim-buster

WORKDIR /app

RUN apt-get update

RUN pip install --upgrade pip

COPY . .

RUN pip3 install -r requirements.txt

RUN mkdir -p logs

EXPOSE 5000

ENTRYPOINT [ "python", "-u", "src/server.py"]