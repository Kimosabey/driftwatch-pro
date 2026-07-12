FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY driftwatch ./driftwatch
ENV PORT=8000
EXPOSE 8000
CMD ["python", "-m", "driftwatch.api"]
