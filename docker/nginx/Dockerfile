#from nginx:1.19-alpine
#
#RUN rm /etc/nginx/conf.d/default.conf
#COPY nginx.conf /etc/nginx/conf.d
from python:3.11

RUN pip3 install --upgrade pip
COPY ./ ./

#COPY ./send_email ./send_email
RUN pip3 install -r requirements.txt

RUN pip3 install gunicorn