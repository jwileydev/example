FROM python:3.10

MAINTAINER James Wiley <https://github.com/jwileydev>


# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt -r requirements.txt

# Mounts the application code to the image
ADD . /django_ec2
WORKDIR /django_ec2

EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

