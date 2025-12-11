# College ERP - Docker Deployment Guide (MySQL)

This guide will help you deploy the College ERP system to your VPS using Docker with remote MySQL database.

## Prerequisites

- A VPS with at least 2GB RAM and 20GB storage
- Docker and Docker Compose installed
- **Remote MySQL database** (version 8.0 or higher recommended)
- Domain name (optional, but recommended for production)

## Installation Steps

### 1. Install Docker on Ubuntu/Debian VPS

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Setup MySQL Database

**On your remote MySQL server**, create the database and user:

```sql
-- Create database
CREATE DATABASE college_erp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (replace with your details)
CREATE USER 'erp_user'@'%' IDENTIFIED BY 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON college_erp.* TO 'erp_user'@'%';
FLUSH PRIVILEGES;
```

**Important MySQL Configuration:**
- Ensure MySQL is configured to accept remote connections
- Update `bind-address` in MySQL config (usually `/etc/mysql/mysql.conf.d/mysqld.cnf`)
- Set `bind-address = 0.0.0.0` (or your VPS IP)
- Restart MySQL: `sudo systemctl restart mysql`
- Allow MySQL port in firewall: `sudo ufw allow 3306/tcp` (if MySQL is on same VPS)

### 3. Clone and Setup Project

```bash
# Clone the repository (or upload via SCP/FTP)
cd /opt
sudo git clone <your-repo-url> college-erp
cd college-erp

# Create environment file
cp .env.example .env
```

### 4. Configure Environment Variables

Edit the `.env` file with your MySQL settings:

```bash
nano .env
```

**Required Configuration:**

```env
# MySQL Connection (IMPORTANT: Update with your MySQL details)
DATABASE_URL=mysql+pymysql://your_user:your_password@your_mysql_host:3306/college_erp

# Example for local MySQL on same VPS:
# DATABASE_URL=mysql+pymysql://erp_user:password123@localhost:3306/college_erp

# Example for remote MySQL:
# DATABASE_URL=mysql+pymysql://erp_user:password123@mysql.example.com:3306/college_erp

# Backend API
SECRET_KEY=<generate with: openssl rand -hex 32>
NEXT_PUBLIC_API_URL=http://your-vps-ip:8000
```

### 5. Build and Run

```bash
# Build and start all services
docker-compose up -d

# Check if services are running
docker-compose ps

# View logs
docker-compose logs -f
```

### 6. Database Setup

```bash
# Run migrations to create tables
docker-compose exec api alembic upgrade head

# (Optional) Seed initial data
docker-compose exec api python scripts/seed.py
```

### 7. Access the Application

- **Frontend**: http://your-vps-ip:3000
- **Backend API**: http://your-vps-ip:8000
- **API Docs**: http://your-vps-ip:8000/docs

## Troubleshooting MySQL Connection

### Test MySQL Connection

```bash
# From your VPS, test MySQL connection
mysql -h your_mysql_host -u your_user -p

# Or using Docker
docker run -it --rm mysql:8.0 mysql -h your_mysql_host -u your_user -p
```

### Common Issues

1. **Connection Refused**
   - Check MySQL `bind-address` setting
   - Verify firewall allows port 3306
   - Ensure MySQL user has remote access (`'user'@'%'`)

2. **Authentication Failed**
   - Verify username/password in `.env`
   - Check MySQL user privileges
   - Try resetting password: `ALTER USER 'user'@'%' IDENTIFIED BY 'newpassword';`

3. **Database Not Found**
   - Verify database exists: `SHOW DATABASES;`
   - Check database name in `DATABASE_URL`

### Check Logs

```bash
# API container logs
docker-compose logs api

# Follow logs in real-time
docker-compose logs -f api
```

## Production Setup with Nginx (Recommended)

### 1. Install Nginx

```bash
sudo apt install nginx -y
```

### 2. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/college-erp
```

Paste this configuration:

```nginx
# API Backend
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Web Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Enable Site and Restart Nginx

```bash
sudo ln -s /etc/nginx/sites-available/college-erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

### 5. Update Environment for Production

Edit `.env`:
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

Restart services:
```bash
docker-compose down
docker-compose up -d
```

## Database Backup (MySQL)

### Manual Backup

```bash
# Backup to local file
mysqldump -h your_mysql_host -u your_user -p college_erp > backup_$(date +%Y%m%d).sql
```

### Automated Backups

Create a backup script:

```bash
nano ~/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/college-erp/backups"
DATE=$(date +%Y%m%d_%H%M%S)
MYSQL_HOST="your_mysql_host"
MYSQL_USER="your_user"
MYSQL_PASSWORD="your_password"
MYSQL_DB="college_erp"

mkdir -p $BACKUP_DIR

mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DB | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

```bash
chmod +x ~/backup-db.sh

# Add to crontab for daily backups at 2 AM
crontab -e
# Add: 0 2 * * * /root/backup-db.sh
```

### Restore Database

```bash
# Restore from backup
gunzip < backup_20240101_020000.sql.gz | mysql -h your_mysql_host -u your_user -p college_erp
```

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f web
```

### Restart Services
```bash
# All services
docker-compose restart

# Specific service
docker-compose restart api
```

### Stop Services
```bash
docker-compose down
```

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

## Security Recommendations

1. **MySQL Security**
   - Use strong passwords
   - Limit access by IP if possible: `CREATE USER 'user'@'vps-ip' IDENTIFIED BY 'pass';`
   - Enable MySQL SSL connections
   - Regular security updates

2. **Application Security**
   - Change default `SECRET_KEY` (use `openssl rand -hex 32`)
   - Use environment variables, never hardcode credentials
   - Regular backups

3. **VPS Firewall**
   ```bash
   sudo ufw allow 22     # SSH
   sudo ufw allow 80     # HTTP
   sudo ufw allow 443    # HTTPS
   sudo ufw enable
   ```

4. **Keep Updated**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

## Performance Tips

1. **MySQL Optimization**
   - Enable query cache
   - Optimize innodb_buffer_pool_size
   - Regular OPTIMIZE TABLE

2. **Connection Pooling**
   - Already configured in SQLModel
   - Adjust pool settings in code if needed

3. **Monitoring**
   - Monitor MySQL slow queries
   - Use `docker stats` to monitor resource usage

## Support

For issues, check:
1. Service logs: `docker-compose logs -f`
2. MySQL connection: `mysql -h host -u user -p`
3. Container status: `docker-compose ps`
4. Network connectivity: `ping your_mysql_host`
