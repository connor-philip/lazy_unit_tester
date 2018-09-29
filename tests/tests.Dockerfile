FROM python:2.7-slim
LABEL maintainer="connor.philip12@hotmail.com"

USER root

WORKDIR /app
ENV PYTHONPATH /app


CMD ["python", "tests/run_tests.py"]
