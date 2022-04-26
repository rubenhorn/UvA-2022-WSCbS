# Use python on alpine as the base image
FROM python:3.9-alpine
# Create a new directory in the image root to store app files and use as working directory
WORKDIR /code
# Copy list of dependencies to image file system
COPY requirements.txt requirements.txt
# Install dependencies using pip (executes at build time)
RUN pip install -r requirements.txt
# Mark default flask port for incoming requests
EXPOSE 5000
# Set flask environment variable to run auth_server.py
ENV FLASK_APP=auth_server
# Only the following layers will be rebuild when the code is changed (this reduces the build time)
# Copy source code to the image file system
COPY auth_server.py .
COPY utils.py .
# Run the flask app (executes at run time)
# Set flask environment variable to allow requests from any host
CMD ["flask", "run", "--host=0.0.0.0"]
