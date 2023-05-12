FROM python:3.6.9-alpine

RUN apk --update --upgrade add --no-cache  \
    gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

RUN python -m pip install --upgrade pip

RUN pip install flask

USER root

CMD [ "python", "src/app.py" ]