FROM xela7/hatpull-base

MAINTAINER Alex Tokar "alext@bitbamboo.com"

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL en_US.UTF-8

RUN mkdir -p /home/docker/run && mkdir -p /home/docker/logs

# install postgresql support for python / tornado
#RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y libpq-dev postgresql-client

# reqs for pycurl
RUN apt-get install -y libcurl4-gnutls-dev librtmp-dev

# install our code
# add from repository root
ADD . /home/docker/code/ 

# setup all the configfiles
RUN ln -s /home/docker/code/server/supervisor.conf /etc/supervisor/conf.d/

# install pip requirements
RUN pip install -vr /home/docker/code/server/requirements.txt 

CMD ["/bin/bash", "/home/docker/code/server/startup.sh"]