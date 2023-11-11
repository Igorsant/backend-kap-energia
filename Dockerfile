FROM joyzoursky/python-chromedriver:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./app.py"]
