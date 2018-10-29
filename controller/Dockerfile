# Build over "alpine"
FROM python:3.7-alpine

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app

# Install all the requirements
RUN pip install --upgrade -r requirements.txt

# How to run it when we start up the box?
CMD ["gunicorn", "-b 0.0.0.0:7072", "-w 4", "Controller:app"]
