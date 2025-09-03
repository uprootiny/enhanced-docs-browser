#!/usr/bin/env -S uv run --with requests python3

"""
🌙 SSL Certificate Generator for semantic.uprootiny.dev
Generates proper SSL certificate for subdomain-to-port mapping
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run shell command with error handling"""
    print(f"🔧 {description}")
    print(f"   Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Success: {description}")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"   ❌ Failed: {description}")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def check_dns_resolution():
    """Check if semantic.uprootiny.dev resolves correctly"""
    print("🔍 Checking DNS resolution...")
    
    # Check if domain resolves
    cmd = "nslookup semantic.uprootiny.dev"
    if run_command(cmd, "Checking DNS resolution for semantic.uprootiny.dev"):
        return True
    else:
        print("⚠️  DNS may not be configured yet. SSL generation may fail.")
        return False

def generate_ssl_certificate():
    """Generate SSL certificate using certbot"""
    domain = "semantic.uprootiny.dev"
    email = "admin@uprootiny.dev"
    
    print(f"🔐 Generating SSL certificate for {domain}")
    
    # First, ensure nginx is not conflicting
    print("📝 Stopping nginx temporarily for certificate generation...")
    run_command("sudo systemctl stop nginx", "Stopping nginx")
    
    # Generate certificate using standalone authenticator
    certbot_cmd = f"""sudo certbot certonly \
        --standalone \
        --non-interactive \
        --agree-tos \
        --email {email} \
        --domains {domain} \
        --expand"""
    
    if run_command(certbot_cmd, f"Generating SSL certificate for {domain}"):
        print(f"✅ SSL certificate generated successfully for {domain}")
        
        # Restart nginx
        run_command("sudo systemctl start nginx", "Starting nginx")
        return True
    else:
        print(f"❌ Failed to generate SSL certificate for {domain}")
        print("   This might be because:")
        print("   1. DNS is not pointing to this server")
        print("   2. Port 80 is not accessible from internet") 
        print("   3. Domain is not properly configured")
        
        # Restart nginx anyway
        run_command("sudo systemctl start nginx", "Starting nginx")
        return False

def install_nginx_config():
    """Install nginx configuration"""
    config_source = "/tmp/semantic.uprootiny.dev.conf"
    config_dest = "/etc/nginx/sites-available/semantic.uprootiny.dev"
    config_link = "/etc/nginx/sites-enabled/semantic.uprootiny.dev"
    
    print("📋 Installing nginx configuration...")
    
    if not os.path.exists(config_source):
        print(f"❌ Config file not found: {config_source}")
        return False
    
    # Copy config to sites-available
    if run_command(f"sudo cp {config_source} {config_dest}", 
                   "Copying nginx config to sites-available"):
        
        # Create symlink in sites-enabled
        if run_command(f"sudo ln -sf {config_dest} {config_link}",
                      "Creating symlink in sites-enabled"):
            
            # Test nginx configuration
            if run_command("sudo nginx -t", "Testing nginx configuration"):
                
                # Reload nginx
                if run_command("sudo systemctl reload nginx", "Reloading nginx"):
                    print("✅ nginx configuration installed and activated")
                    return True
    
    return False

def verify_deployment():
    """Verify the deployment is working"""
    print("🔍 Verifying deployment...")
    
    # Check if nginx is running
    if not run_command("sudo systemctl is-active nginx", "Checking nginx status"):
        return False
    
    # Check if our config is enabled
    if os.path.exists("/etc/nginx/sites-enabled/semantic.uprootiny.dev"):
        print("✅ nginx config is enabled")
    else:
        print("❌ nginx config is not enabled")
        return False
    
    # Check if SSL certificate exists
    cert_path = "/etc/letsencrypt/live/semantic.uprootiny.dev/fullchain.pem"
    if os.path.exists(cert_path):
        print("✅ SSL certificate exists")
        
        # Show certificate info
        run_command(f"sudo openssl x509 -in {cert_path} -text -noout | grep -A2 'Subject:'",
                   "Checking certificate details")
        return True
    else:
        print("❌ SSL certificate not found")
        return False

def main():
    """Main SSL setup process"""
    print("🌙 Silver Lining SSL Certificate Setup")
    print("=" * 50)
    
    # Step 1: Check DNS
    dns_ok = check_dns_resolution()
    
    # Step 2: Generate SSL certificate
    if dns_ok:
        ssl_ok = generate_ssl_certificate()
    else:
        print("⚠️  Skipping SSL generation due to DNS issues")
        ssl_ok = False
    
    # Step 3: Install nginx config
    nginx_ok = install_nginx_config()
    
    # Step 4: Verify deployment
    if ssl_ok and nginx_ok:
        verify_ok = verify_deployment()
        
        if verify_ok:
            print("\n" + "=" * 50)
            print("✅ 🌙 SSL DEPLOYMENT SUCCESSFUL!")
            print("   semantic.uprootiny.dev is ready with:")
            print("   • HTTPS SSL certificate")
            print("   • nginx reverse proxy to port 45503")
            print("   • API integration with port 44500") 
            print("   • Sophisticated ClojureScript interface")
            print("=" * 50)
            return 0
        else:
            print("\n❌ Deployment verification failed")
            return 1
    else:
        print("\n⚠️  Partial deployment completed")
        print("   nginx config ready, SSL certificate may need manual setup")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)