FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY api_gateway/ .
COPY common/ common/

EXPOSE 5000

CMD ["python", "app.py"]
