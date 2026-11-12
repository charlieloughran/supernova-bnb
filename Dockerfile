FROM python:3.13

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn==23.0.0

COPY app.py .
COPY lib/ ./lib/
COPY templates/ ./templates/
COPY static/ ./static/

EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
