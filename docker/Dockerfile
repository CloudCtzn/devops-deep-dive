FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY job_tracker.py .

CMD ["python", "job_tracker.py"]

