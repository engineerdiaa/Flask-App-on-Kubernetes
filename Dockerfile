FROM python:3.9-slim

WORKDIR /app

# Install Libraries
RUN pip install flask pymongo

# Copy your code and the JSON file
COPY app.py .
COPY bookstore.json .

# Expose the Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]