# Use the official Python base image
FROM python:3.11

# set the working directory inside the container
WORKDIR /hudson

# Install the required Python dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD tail -f /dev/null