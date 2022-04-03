# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements/ /code/requirements/

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements/dev.txt

# 
COPY . /code/

# 
CMD ["uvicorn", "api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]