FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY req.txt /app/
RUN pip install --no-cache-dir -r req.txt
COPY . /app/
EXPOSE 8000
WORKDIR /app/stations