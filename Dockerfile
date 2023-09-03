FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /jkh
ADD . /jkh
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate