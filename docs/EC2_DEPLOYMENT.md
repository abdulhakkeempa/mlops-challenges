## Deploying FastAPI Applications on Amazon Linux using Uvicorn and Nginx

This guide outlines the steps to deploy a FastAPI application on an Amazon Linux instance using Uvicorn as the ASGI server and Nginx as a reverse proxy.

**1. Set up the Virtual Environment and Install Dependencies:**

```
python3 -m venv fastapi-venv
source fastapi-venv/bin/activate
pip install fastapi uvicorn # Add other necessary dependencies
```

**2. Run the FastAPI Application (for testing):**
```
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**3. Create a Systemd Service File:**
```sudo nano /etc/systemd/system/fastapi.service```

```
[Unit]
Description=FastAPI Application Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/<project_directory>
ExecStart=/home/ec2-user/<project_directory>/fastapi-venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

**4. Manage the Systemd Service:**
```
sudo systemctl daemon-reload
sudo systemctl start fastapi
sudo systemctl enable fastapi
sudo systemctl status fastapi
```

**5. Install and Enable Nginx:**
```
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

**6. Configure Nginx as a Reverse Proxy:**
```sudo nano /etc/nginx/conf.d/fastapi.conf```

```
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_IP; # Or your_domain.com

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**7. Test and Restart Nginx:**
```
sudo nginx -t
sudo systemctl restart nginx
```

**8. (Optional) Set up HTTPS with Certbot:**
```
sudo yum install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your_domain.com # Replace with your actual domain
```

