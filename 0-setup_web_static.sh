#!/usr/bin/env bash
#this script configures nginx in a new server
sudo apt-get -y update
sudo apt-get -y install nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sed -i '/listen 80 default_server;/a location /hbnb_static/ { alias /data/web_static/current/; autoindex off;}' /etc/nginx/sites-available/default
sudo service nginx restart
