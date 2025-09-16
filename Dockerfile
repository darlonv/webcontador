FROM python:3.12-slim

# injeta a "versão" (git SHA/tag) no build
ARG VERSION=dev
ENV APP_VERSION=$VERSION \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./app.py
COPY templates ./templates

EXPOSE 8000
CMD ["python", "app.py"]
