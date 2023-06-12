FROM python:3.9
RUN apt-get update
RUN apt-get install -y zip
RUN mkdir /back
RUN mkdir /logs
RUN mkdir /django_out
WORKDIR /back
ADD requirements.txt /back/
RUN pip install -r requirements.txt
ADD . /back/
EXPOSE 8000
CMD ["/bin/bash", "/back/entrypoint.sh"]