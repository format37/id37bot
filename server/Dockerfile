# Use Python 3.9 image as the base
FROM python:3.9

# Set the working directory
WORKDIR /server

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the server.py file
COPY server.py .

# Run the server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8706"]