# Use Python 2.7 on Debian Bullseye instead of Alpine/Buster
FROM python:2.7-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kubedashboard.wsgi:application"]