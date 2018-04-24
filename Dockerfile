FROM python:3
ENV PYTHONUNBUFFERED 1
# RUN mkdir /mixeddit
WORKDIR /mixeddit
ADD . .
# ADD requirements.txt .
RUN pip install -r requirements.txt
