FROM --platform=linux/amd64 python:3.9-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask" ,"run", "--host=0.0.0.0"]