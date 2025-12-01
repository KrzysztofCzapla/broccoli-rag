FROM python:3.10-slim

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt update
RUN apt install -y make curl

COPY ./src .

ENV PYTHONPATH=/

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload", "--reload-dir", "/src", "--reload-include", "*.sql"]