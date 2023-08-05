# Use the Python base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock into the container's working directory
COPY Pipfile Pipfile.lock /app/

# Install pipenv inside the container
RUN pip install pipenv

# Install dependencies from Pipfile.lock
RUN pipenv install --system --deploy

# Copy the rest of your project files into the container
COPY . /app/

# Set the entry point for the container to run your main Python script
CMD ["python", "personal_helper.py"]
