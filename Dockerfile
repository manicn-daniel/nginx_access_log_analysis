FROM bitnami/spark:latest

COPY . /app
WORKDIR /app

CMD ["spark-submit", "--master", "local[*]", "log_analysis.py"]
