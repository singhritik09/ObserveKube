FROM python:2.7.18-alpine

WORKDIR /app

# Install system dependencies for compiling Python packages
RUN apk add --no-cache \
    build-base \
    musl-dev \
    libffi-dev \
    openssl-dev \
    gcc \
    g++ \
    make \
    python2-dev \
    libxml2-dev \
    libxslt-dev \
    postgresql-dev

# Upgrade pip, setuptools, wheel
RUN python -m ensurepip \
    && python -m pip install --upgrade pip setuptools wheel

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

EXPOSE 9000
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "kubedashboard.wsgi:application"]