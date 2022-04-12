
# pull official base image
FROM python:3.9.2-slim-buster

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt install -y netcat


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements ./requirements
RUN pip install -r requirements/dev.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]