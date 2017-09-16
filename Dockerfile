############################################################
# Dockerfile to run a Django-based web application
# Based on an AMI
############################################################
# Set the base image to use to Ubuntu
FROM phusion/baseimage:0.9.22

# Set the file maintainer (your name - the file's author)
MAINTAINER Jonathan Anderson

CMD ["/sbin/my_init"]

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y python3-dev
RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y git
RUN apt-get install -y nginx
# Create application subdirectories
WORKDIR /srv
RUN mkdir media static logs
#read
VOLUME ["/srv/media/", "/srv/logs/"]
# Copy application source code to SRCDIR
COPY ./docker-entrypoint.sh /etc/my_init.d/
RUN ["git", "init"]
RUN ["git", "remote", "add", "origin", "https://github.com/I-sektionen/i-portalen"]
RUN ["git", "fetch", "origin", "docker:refs/remotes/origin/master"]
RUN ["git", "checkout", "-t", "origin/master"]
RUN rm -f /etc/service/nginx/down &&\
  rm /etc/nginx/sites-enabled/default

# Install Python dependencies
#RUN pip3 $DOCKYARD_SRVPROJ/requirement.txt
# Port to expose
EXPOSE 80
# Copy entrypoint script into the image
RUN /usr/bin/pip3 install --upgrade pip
RUN /usr/bin/pip3 install -r requirements.txt
RUN /usr/bin/pip3 install gunicorn

RUN ["cp", "./django_nginx.conf", "/etc/nginx/sites-available/"]
#COPY ./django_nginx_local.conf /etc/nginx/sites-available/django_nginx.conf
RUN ["chmod", "+x", "/etc/my_init.d/docker-entrypoint.sh"]

WORKDIR /srv/wsgi

RUN ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*