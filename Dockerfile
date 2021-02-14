FROM python:3.6.9
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
