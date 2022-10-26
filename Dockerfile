FROM python:3.9

WORKDIR /apps
ADD requirements.txt /apps/
RUN pip install -r /apps/requirements.txt
ADD *.py /apps/
EXPOSE 8000
CMD /usr/local/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app