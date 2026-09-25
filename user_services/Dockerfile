FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY user_services/ .
COPY common/ common/

EXPOSE 5002

CMD ["python", "app.py"]
