# Use the official Python base image for FastAPI

 FROM python:3.10.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the  LR_pipeline.joblib files to the container
COPY pipeline.joblib .

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that the FastAPI application will run on
EXPOSE 7860

# Command to run the FastAPI application when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]










