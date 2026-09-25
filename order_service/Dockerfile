FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY order_service/ .
COPY common/ common/

EXPOSE 5003

CMD ["python", "app.py"]
