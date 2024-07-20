FROM --platform=linux/amd64 python:3.10

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8003

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
