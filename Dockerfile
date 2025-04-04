# build container
FROM python:3-alpine as build
WORKDIR /usr/src/app

RUN apk add --no-cache --update python3-dev musl-dev gcc libc-dev linux-headers alpine-sdk git cargo rust && rm -rf /var/cache/apk/*

COPY .git .
COPY .env.template .
RUN [ -e "/usr/src/app/.env" ] && echo "Env already exists" || mv .env.template .env
RUN sed -i "s/%VER%/$(git describe --always --abbrev | sed 's/-/./')/" .env


RUN adduser -s /bin/bash -S service
USER service
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# main container
FROM python:3-alpine as order
ENV PYTHONUNBUFFERED definitely
ENV TZ Europe/Vienna
WORKDIR /usr/src/app

RUN adduser -s /bin/bash -S service && chown service:root /usr/src/app
COPY --from=build /home/service/.local/lib/python3.*/site-packages /home/service/.local/lib/python/site-packages
RUN mkdir --parents  /home/service/.local/lib/python$(python --version | sed -e 's/[^0-9.]//g' | cut -f1,2 -d'.'); \
        mv /home/service/.local/lib/python/site-packages /home/service/.local/lib/python$(python --version | sed -e 's/[^0-9.]//g' | cut -f1,2 -d'.')/site-packages;\
        rmdir /home/service/.local/lib/python
USER service

COPY --from=0 /usr/src/app/.env .
COPY main.py ./
COPY src/ ./src

CMD ["python", "main.py"]
