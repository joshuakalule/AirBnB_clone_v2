#!/usr/bin/env bash
# install nginx and add new server block to the configuration

# check and install if nginx does not exist
if ! command -v nginx &> /dev/null; then
    echo "NGINX not installed. Installing now.."

    # installation of nginx
    apt-get -y update
    apt-get -y install nginx
    ufw allow 'Nginx HTTP'
    echo 'Hello World!' > /var/www/html/index.nginx-debian.html
    service nginx start

    echo "NGINX installation successfull"
else
    echo "NGINX already installed"
fi

# function to check if file exists otherwise create file
dir_exists() {
    if [ ! -d "$1" ]; then
        mkdir "$1"
    else
        echo "Directory '$1' already exists"
    fi
}

# files to check existence otherwise create
dirs=(
    "/data/"
    "/data/web_static/"
    "/data/web_static/releases/"
    "/data/web_static/shared/"
    "/data/web_static/releases/test/"
)

for dir in "${dirs[@]}"; do
    dir_exists "$dir"
done

# put simple text into index.html for testing
echo "\
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# create symbolic link to folder /data/web_static/releases/test/
#+ if it doesn't exist
sym_link="/data/web_static/current"
linked_dir="/data/web_static/releases/test/"
if [ -L "$sym_link" ]; then
    rm "$sym_link"
fi
ln -s "$linked_dir" "$sym_link"
echo "symbolic link created"

# give recursive ownership of /data/ to ubuntu and group
chown -R ubuntu:ubuntu /data

NGINX_CONFIG=\
"server {
        listen 80;
        listen [::]:80;

        server_name onepimeht.tech;

        location /hbnb_static/ {
                alias /data/web_static/current/;
                try_files \$uri \$uri/ =404;
        }
}"

bash -c "echo -e '$NGINX_CONFIG' > /etc/nginx/sites-enabled/hbnb_static"

# enable the site and restart
ln -s /etc/nginx/sites-available/hbnb_static /etc/nginx/sites-enabled/

# Check if the include line already exists in the existing configuration
if ! grep -q "include $new_config;" "$existing_config"; then
    # Add the include line to the existing configuration
    echo "include $new_config;" | tee -a "$existing_config"
fi

service nginx restart