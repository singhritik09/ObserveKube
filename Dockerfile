FROM python:2.7.18-alpine

WORKDIR /app

# Install build tools and dependencies
RUN apk add --no-cache build-base libffi-dev openssl-dev

# Upgrade pip to latest compatible for Python 2.7
RUN python -m ensurepip \
    && python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "kubedashboard.wsgi:application"]