FROM registry.centos.org/centos/centos:7

LABEL maintainer="thrcka@redhat.com"

ENV LANG=en_US.UTF-8

# install repositories for latest stable origin and PostgreSQL 9.4 
RUN yum --setopt=tsflags=nodocs install -y epel-release centos-release-openshift-origin && \
    yum --setopt=tsflags=nodocs install -y https://download.postgresql.org/pub/repos/yum/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-3.noarch.rpm &&\
    yum --setopt=tsflags=nodocs install -y postgresql awscli awk pwgen origin-clients &&\
    yum clean all

RUN mkdir -p /home/deployer/

COPY env.sh deploy.sh secrets-template.yaml config-template.yaml /home/deployer/

WORKDIR /home/deployer

CMD ["./deploy.sh"]
