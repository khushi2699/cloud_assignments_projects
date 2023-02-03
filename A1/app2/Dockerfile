FROM python:3-alpine3.15
WORKDIR /app2
COPY . /app2
RUN pip install -r requirements.txt
ENV FLASK_APP=app2.py
ENV FLASK_ENV=development
EXPOSE 5001
CMD ["python3", "-m", "flask","run","--host=0.0.0.0" , "-p", "5001"]