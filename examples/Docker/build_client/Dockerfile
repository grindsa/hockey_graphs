FROM ubuntu:20.04
LABEL maintainer="grindelsack@gmail.com"

RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install --no-install-recommends -y \
    curl \
    npm \
    openssh-client \
    rsync

RUN mkdir -p /tmp/ui/src
RUN mkdir -p /tmp/rest/functions
RUN mkdir -p /tmp/rest/tools
RUN mkdir -p /tmp/static

COPY ui /tmp/ui
COPY locale /tmp/locale
COPY rest/functions/*.py /tmp/rest/functions/
COPY rest/*.py /tmp/rest/
COPY rest/tools/*.py /tmp/rest/tools/
COPY static/img/. /tmp/static/img/

COPY examples/Docker/build_client/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+rx /docker-entrypoint.sh

WORKDIR /tmp/

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["sh"]
