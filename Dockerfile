FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["orpheus-api"]
