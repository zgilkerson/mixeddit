FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /mixeddit
ADD . .
RUN pip install -r requirements.txt
