FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /jkh
ADD . /jkh
RUN pip install -r requirements.txt
