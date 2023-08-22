FROM python:3.10-slim

# It is required to keep the pip up to date.
RUN pip install --upgrade pip

# Env variables
# Prints logs in container
ENV PYTHONUNBUFFERED=1

# Set the Working directory
WORKDIR /app

# Copy the files
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 5003

# Running the executor file.
# Note We need to separate it rather than keeping it in one command
CMD [ "python", "main.py" ]