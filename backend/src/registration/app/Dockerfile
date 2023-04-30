FROM python:3.7.2

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn","--chdir", "registration\.API", "registration\.API:registration\.API", "-b", "0.0.0.0:8000"]