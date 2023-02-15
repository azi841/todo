FROM python:3.10.10
WORKDIR /flask
COPY ./requirements.txt /flask
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=server.py
CMD ["flask", "run", "--host", "0.0.0.0"]