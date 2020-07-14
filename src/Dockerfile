FROM python:3.8.0-alpine

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/

ENTRYPOINT python manage.py collectstatic --noinput --clear && python manage.py makemigrations --noinput && python manage.py migrate --noinput && gunicorn SurCTF.wsgi:application --bind 0.0.0.0:8000 --workers=3 --threads=3

EXPOSE 8000