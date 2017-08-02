# BOTLIB - Framework to program bots
#
#

FROM ubuntu
ENV PYTHONPATH .
EXPOSE 10102
STOPSIGNAL 9
MAINTAINER bthate@dds.nl

RUN apt-get update 
RUN apt-get -y install apt-utils
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install bash
RUN apt-get -y install ircd-ircu
RUN apt-get -y install ejabberd
RUN pip3 install --upgrade pip
ADD . run
WORKDIR run
RUN python3 setup.py install

#RUN pip3 install -f dist/*
RUN echo "flitser34" > ./.sleekpass

SHELL ["/bin/bash"]
CMD ["service", ircd-ircu", "start"]
CMD ["service", "ejabberd", "start"]
CMD ["bot", "-u", "-a", "-d", "data"]
