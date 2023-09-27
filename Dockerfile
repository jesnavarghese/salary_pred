FROM python:latest
WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y
RUN pip install -r requirement.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

CMD ["python3", "app.py"]