FROM alpine:3.14
RUN apk add zsh python3
RUN python3 -m ensurepip

# SHAPELY
RUN apk --update add build-base libxslt-dev python3-dev
# build geos
RUN apk add --virtual .build-deps \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
  gcc libc-dev geos-dev geos && \
  runDeps="$(scanelf --needed --nobanner --recursive /usr/local \
  | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
  | xargs -r apk info --installed \
  | sort -u)" && \
  apk add --virtual .rundeps $runDeps
RUN geos-config --cflags

# POSTGRESQL
RUN apk --update add postgresql-client postgresql-dev


ENTRYPOINT ["sleep", "infinity"]
