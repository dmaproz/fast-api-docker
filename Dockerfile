FROM python:3.10-alpine3.23
COPY requirements.txt /tmp

RUN pip install --upgrade -r /tmp/requirements.txt

COPY ./app /app
CMD python /app/app.py