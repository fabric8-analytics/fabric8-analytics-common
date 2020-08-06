FROM registry.centos.org/centos/centos:7


ENV LANG=en_US.UTF-8 \
    NOVENV=1
ARG var

ENV FIREBASE_API_KEY=$var

RUN yum install -y epel-release &&\
    yum install -y gcc which python36-pip python36-devel python36-virtualenv git &&\
    mkdir -p /tests

COPY . /tests
RUN pushd /tests &&\
    pip3 install -r requirements.txt

WORKDIR /tests
ENTRYPOINT ["/tests/dashboard.sh"]

