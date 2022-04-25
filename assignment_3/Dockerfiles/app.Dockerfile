FROM python:3.9-alpine
WORKDIR /code
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000

ENV FLASK_APP=app_server
COPY app_server.py .
COPY utils.py .
CMD ["flask", "run", "--host=0.0.0.0"]