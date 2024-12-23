FROM python:3-slim

WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the application code into the container
COPY app.py .

ENV MINIO_ACCESS_KEY=myaccesskey
ENV MINIO_SECRET_KEY=mysecretkey

CMD ["python", "app.py"]
# Launch the app


