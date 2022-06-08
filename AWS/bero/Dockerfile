FROM python:3.8-slim-buster

WORKDIR /app  

COPY requirements.txt .

RUN apt-get update

RUN apt-get -y install curl

RUN apt-get -y install sudo

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

RUN sudo apt-get install -y nodejs


RUN apt-get -y install awscli



RUN npm install -g aws-cdk

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 7001

CMD ["python", "api.py"]
