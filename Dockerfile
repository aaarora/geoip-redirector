FROM opensciencegrid/software-base:fresh
LABEL maintainer OSG Software <help@opensciencegrid.org>

RUN yum -y install vim emacs && \
    yum -y install mod_wsgi

ADD geoip.conf /etc/httpd/conf.d/geoip.conf
ADD supervisord.conf /etc/supervisord.d/
ADD image-config.d/* /etc/osg/image-config.d/
ADD geoip.py /var/www/python/geoip.py