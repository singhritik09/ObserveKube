FROM python:2.7.18-alpine

WORKDIR /app

RUN apk add --no-cache build-base

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "kubedashboard.wsgi:application"]