FROM registry.centos.org/sclo/postgresql-94-centos7:latest
MAINTAINER Fridolin Pokorny <fridolin@redhat.com>

ADD ./common.sh /usr/share/container-scripts/postgresql/common.sh

EXPOSE 5432
CMD ["run-postgresql"]
