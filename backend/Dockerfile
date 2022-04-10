
# pull official base image
FROM python:3.9

# set work directory
WORKDIR /code

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/ /code/requirements/
RUN pip install --no-cache-dir --upgrade -r /code/requirements/dev.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]