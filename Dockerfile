FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["gunicorn", "eIntern.wsgi:application", "--bind", "0.0.0.0:8000"]
