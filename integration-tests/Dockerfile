FROM registry.centos.org/centos/centos:7
MAINTAINER Michal Srb <michal@redhat.com>

ENV LANG=en_US.UTF-8 \
    NOVENV=1

RUN yum install -y epel-release &&\
    yum install -y gcc which python34-pip python34-devel centos-release-openshift-origin36 &&\
    mkdir -p /tests

COPY . /tests
RUN pushd /tests &&\
    pip3 install -r requirements.txt

WORKDIR /tests
ENTRYPOINT ["/tests/runtest.sh"]

