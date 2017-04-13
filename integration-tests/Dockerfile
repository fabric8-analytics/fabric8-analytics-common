FROM registry.centos.org/centos/centos:7
MAINTAINER Jiri Popelka <jpopelka@redhat.com>

ENV LANG=en_US.UTF-8 \
    IT_PATH='/opt/integration-tests' \
    NOVENV=1

RUN useradd integration

RUN yum install -y epel-release && \
    yum install -y python34-devel python34-pip which && \
    yum clean all

COPY ./requirements.txt /tmp/install/
RUN pip3 install -r /tmp/install/requirements.txt && \
    rm -rf /tmp/install/

COPY . ${IT_PATH}

WORKDIR ${IT_PATH}
USER integration
CMD ["./runtest.sh", "-D", "openshift=true", "-D", "breath_time=30"]
