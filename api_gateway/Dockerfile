FROM python:3.7.2-stretch


# Set the working directory to /app
WORKDIR /home/microservice

# Copy the current directory contents into the container at /home/dashboard
COPY . .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uwsgi", "--py-autoreload", "1",  "app.ini"]