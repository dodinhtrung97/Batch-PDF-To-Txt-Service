# Use slim because it has gcc
FROM python:3.7-slim

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app

# Install all the requirements
RUN pip install --upgrade -r requirements.txt

# How to run it when we start up the box?
CMD ["python", "-u", "Controller.py"]
