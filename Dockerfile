FROM tomgruner/globallometree-base

MAINTAINER Tom Gruner "tom.gruner@gmail.com"

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL en_US.UTF-8

RUN mkdir -p /opt/run && mkdir -p /opt/logs

# install postgresql support for python / tornado
#RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y libpq-dev postgresql-client

# reqs for pycurl
RUN apt-get install -y libcurl4-gnutls-dev librtmp-dev

# install our code
# add from repository root
ADD . /opt/code/ 

# install pip requirements
RUN pip install -vr /opt/code/server/requirements.txt 

CMD ["/bin/bash", "/opt/code/server/startup.sh"]