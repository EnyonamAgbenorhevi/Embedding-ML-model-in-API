# Use the official Python base image for FastAPI
FROM python:3.10.11

# Set the working directory in the container
WORKDIR /app


# Copy the requirements file into the container
COPY ./requirements.txt /app


# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire src directory into the container
COPY ./src  /app/src


# Expose the port that your FastAPI application will run on (default is 8000)
EXPOSE 8000

# Define the command to run your FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]







