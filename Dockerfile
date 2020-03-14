FROM ubuntu:18.04

ARG username
ARG password

RUN apt-get update && apt-get -y install apache2 apache2-utils

RUN apt-get -y install libcgi-pm-perl libdatetime-perl libdbd-mysql-perl libdbi-perl libgd-graph-perl

RUN ln -s /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/

COPY includes/index.html /var/www/html/index.html
COPY grapher.cgi /usr/lib/cgi-bin/grapher.cgi
COPY rfas.cgi /usr/lib/cgi-bin/rfas.cgi

WORKDIR /usr/rfas
COPY includes/rfas_functions.pl /usr/rfas/rfas_functions.pl
COPY includes/rfas_config.pl /usr/rfas/rfas_config.pl
COPY includes/website.conf /etc/apache2/sites-available/000-default.conf


COPY includes/db-setup.pl /usr/rfas/db-setup.pl
COPY includes/route_feedback.sql /usr/rfas/route_feedback.sql

RUN chmod 755 /usr/lib/cgi-bin/grapher.cgi
RUN chmod 755 /usr/lib/cgi-bin/rfas.cgi

RUN htpasswd -b -c /etc/apache2/.htpasswd $username $password

EXPOSE 80

CMD /usr/sbin/apache2ctl -D FOREGROUND
