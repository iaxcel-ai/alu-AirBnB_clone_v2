#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx > /dev/null 2>&1; then
    sudo apt-get update -y
    sudo apt-get install -y nginx
fi

# Create necessary folders if they don't already exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
sudo bash -c 'cat > /data/web_static/releases/test/index.html' << EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create/recreate the symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve /data/web_static/current/ at /hbnb_static
if ! grep -q "hbnb_static" /etc/nginx/sites-enabled/default; then
    sudo sed -i '/listen 80;/a\    location /hbnb_static {\n        alias /data/web_static/current/;\n    }' /etc/nginx/sites-enabled/default
fi

# Restart Nginx
sudo service nginx restart

exit 0
