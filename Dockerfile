FROM python:2.7.10

WORKDIR /nyaa
VOLUME [ "/nyaa" ]

RUN pip install feedparser simplejson
CMD [ "python", "nyaa.py" ]
