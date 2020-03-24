FROM python:3.6-alpine

# allow stdout to console
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv
COPY Pipfile* /
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /
WORKDIR /
COPY . /

# ? are these lines necessary ?
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user
