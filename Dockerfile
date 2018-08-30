FROM registry.centos.org/centos/centos:7

MAINTAINER Pavel Tisnovsky <ptisnovs@redhat.com>

RUN yum install -y epel-release && \
    yum install -y python34-devel python34-pip gcc which && \
    yum clean all && \
    rm -rf /var/cache/yum && \
    pip3 install virtualenv && \
    pip3 install --upgrade pip && \
    mkdir /taas

COPY ./ /taas

WORKDIR /taas/taas

RUN pip3 install -r requirements.txt

CMD ["./run_taas_in_docker.sh"]
