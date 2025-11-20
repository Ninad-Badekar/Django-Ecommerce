FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN apt-get update && apt-get install -y default-mysql-client
    
RUN pip install mysqlclient


# Collect static files
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "shoe_store.wsgi:application", "--bind", "0.0.0.0:8000"]
