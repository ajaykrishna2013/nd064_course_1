FROM python:2.7

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x run.sh

EXPOSE 7111

CMD ["./run.sh"]
