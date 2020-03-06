FROM ubuntu:18.04

RUN apt-get update && apt-get -y install apache2

RUN apt-get -y install libcgi-pm-perl libdatetime-perl libdbd-mysql-perl libdbi-perl libgd-graph-perl

RUN ln -s /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/

COPY includes/index.html /var/www/html/index.html
COPY grapher.cgi /usr/lib/cgi-bin/grapher.cgi
COPY rfas.cgi /usr/lib/cgi-bin/rfas.cgi
COPY includes/rfas_config.pl /usr/config/rfas_config.pl

WORKDIR /usr/setup
COPY includes/db-setup.pl /usr/setup/db-setup.pl

RUN chmod 755 /usr/lib/cgi-bin/grapher.cgi
RUN chmod 755 /usr/lib/cgi-bin/rfas.cgi

EXPOSE 80

CMD /usr/sbin/apache2ctl -D FOREGROUND
