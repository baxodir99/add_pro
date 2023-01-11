FROM python:3.7-alpine
WORKDIR /app
COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]