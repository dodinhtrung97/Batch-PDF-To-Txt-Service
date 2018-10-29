# Use slim to fix moviepy issues
FROM python:3.7-slim

# Copy everthing from . to /app inside the 'box'
COPY . /app
WORKDIR /app

# Install all the requirements
RUN pip install --upgrade -r requirements.txt

# Generate random number to ensure no duplicate name so that rq worker will work with --scale command
CMD number=`shuf -i 1-100000 -n 1` && rq worker pdf --name $number --url redis://redis:6379