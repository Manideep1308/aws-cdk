FROM python:3.7-alpine


WORKDIR /app.py


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app.py/


CMD ["python", "app.py"]
