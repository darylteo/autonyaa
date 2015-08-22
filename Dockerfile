FROM python:2.7.10

WORKDIR /nyaa

VOLUME [ "/nyaa/target", "/nyaa/configs" ]

RUN pip install feedparser simplejson
CMD [ "python", "nyaa.py" ]

COPY nyaa.py settings.json /nyaa/
