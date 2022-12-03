FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY round_analytics/ .

CMD ["python", "main.py"]
