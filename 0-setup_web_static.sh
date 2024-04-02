#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# ensure ngnix is installed
if ! command nginx -v &> /dev/null; then
    apt-get -y update
    apt-get -y install nginx
fi

# ensure presence of these directories
declare -a DIRS=(
    "/data/"
    "/data/web_static/"
    "/data/web_static/releases/"
    "/data/web_static/shared/"
    "/data/web_static/releases/test/"
)
for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
done

# create fake html file to test ngnix install
echo "Nginx installed successfully!" > /data/web_static/releases/test/index.html

# ensure symbolic link is up-to date
ln -sf "/data/web_static/releases/test/" "/data/web_static/current"

# set ownership
chown --recursive --no-dereference ubuntu:ubuntu /data/

# Update Nginx config to serve content of /data/web_static/current/ to
# hbnb_static
# Desccription: ensures this location block is added within the server block 
# but before the first location block
TMP_FILE_PATH="/tmp/tmp_file"
CONFIG_FILE="/etc/nginx/sites-available/default"
echo "" > "$TMP_FILE_PATH"
TRIGGER=0
ENTRY="
    location /hbnb_static {
        alias /data/web_static/current/;
    }"
while IFS= read -r line; do
	if [[ "$line" =~ [[:space:]]*server[[:space:]]+\{ && "$TRIGGER" == 0 ]]; then
		TRIGGER=1
	fi
	
	if [[ "$TRIGGER" == 1 && "$line" =~ [[:space:]]*location ]]; then
		echo -e "$ENTRY\n$line" >> "$TMP_FILE_PATH"
		TRIGGER=-1
	else
		echo "$line" >> "$TMP_FILE_PATH"
	fi
done < "$CONFIG_FILE"
cat "$TMP_FILE_PATH" > "$CONFIG_FILE"
#restart nginx
service nginx restart
