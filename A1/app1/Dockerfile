FROM python:3-alpine3.15
WORKDIR /app1
COPY . /app1
RUN pip install -r requirements.txt
ENV FLASK_APP=app1.py
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["python3", "-m", "flask","run","--host=0.0.0.0"]