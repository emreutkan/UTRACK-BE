#!/bin/bash
set -e

echo "Starting Bootstrap"

# 1. Set variables
PROJECT_DIR="/home/ubuntu/utrack-backend"
REPO_URL="https://github.com/emreutkan/utrack-be"

# 2. Install system dependencies
echo "Installing system packages..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.12 python3.12-venv python3-pip postgresql postgresql-contrib git libpq-dev python3-dev nginx

# 3. Clone repository
echo "Cloning repository..."
if [ ! -d "$PROJECT_DIR" ]; then
  sudo mkdir -p "$PROJECT_DIR"
  sudo chown ubuntu:ubuntu "$PROJECT_DIR"
  git clone "$REPO_URL" "$PROJECT_DIR"
else
  echo "Repository already exists, skipping clone..."
fi

cd "$PROJECT_DIR"

# 4. Create venv
echo "Creating virtual environment"
if [ ! -d "venv" ]; then
  python3.12 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt gunicorn psycopg2-binary

# 5. Get secrets from environment or GitHub (you'll need to set these)
DB_NAME="${DB_NAME:-utrack_db}"
DB_USER="${DB_USER:-utrack_user}"
DB_PASSWORD="${DB_PASSWORD}"
SECRET_KEY="${SECRET_KEY}"
ALLOWED_HOSTS="${ALLOWED_HOSTS:-*}"

# Validate required secrets
if [ -z "$DB_PASSWORD" ]; then
  echo "ERROR: DB_PASSWORD is required!"
  exit 1
fi

if [ -z "$SECRET_KEY" ]; then
  echo "ERROR: SECRET_KEY is required!"
  exit 1
fi

# 6. Setup PostgreSQL database
echo "Setting up PostgreSQL database"
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
  sudo -u postgres psql <<EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
EOF
  echo "Database created!"
else
  echo "Database already exists!"
fi

# 7. Setup Gunicorn systemd service
echo "Setting up Gunicorn service"
sudo tee /etc/systemd/system/utrack.service > /dev/null <<EOF
[Unit]
Description=UTrack Django application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
Environment="SECRET_KEY=$SECRET_KEY"
Environment="DEBUG=False"
Environment="DB_NAME=$DB_NAME"
Environment="DB_USER=$DB_USER"
Environment="DB_PASSWORD=$DB_PASSWORD"
Environment="DB_HOST=localhost"
Environment="DB_PORT=5432"
Environment="ALLOWED_HOSTS=$ALLOWED_HOSTS"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:$PROJECT_DIR/utrack.sock \
    --timeout 120 \
    utrack.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 8. Setup Nginx configuration
echo "Setting up Nginx"
EC2_HOST="${EC2_HOST:-_}"
sudo tee /etc/nginx/sites-available/utrack > /dev/null <<EOF
server {
    listen 80;
    server_name $EC2_HOST;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/utrack.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    client_max_body_size 100M;
}
EOF

# 9. Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/utrack /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 10. Set permissions
echo "Setting permissions"
sudo chmod 755 /home/ubuntu
sudo chmod 755 "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/media"
sudo chown -R ubuntu:www-data "$PROJECT_DIR"
sudo chmod -R 775 "$PROJECT_DIR/media"
sudo chmod -R 775 "$PROJECT_DIR/logs"

# 11. Enable and start services
echo "Starting services"
sudo systemctl daemon-reload
sudo systemctl enable utrack

if sudo nginx -t; then
  sudo systemctl enable nginx
  sudo systemctl restart nginx
else
  echo "Error: Nginx configuration error!"
  exit 1
fi

echo "Bootstrap completed successfully!"
echo "Note: Run migrations and collectstatic manually or via deploy workflow"

