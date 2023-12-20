import subprocess
import os
import shutil
import urllib.request
import tarfile

# NGINX version
nginx_version = "1.18.1"

# Clone ModSecurity module
subprocess.run(["git", "clone", "--depth", "1", "https://github.com/SpiderLabs/ModSecurity-nginx.git"])

# Get NGINX version on the host
nginx_version_output = subprocess.check_output(["nginx", "-v"]).decode("utf-8")
installed_nginx_version = nginx_version_output.split("/")[1].strip()

# Download NGINX source code
nginx_source_url = f"http://nginx.org/download/nginx-{installed_nginx_version}.tar.gz"
urllib.request.urlretrieve(nginx_source_url, f"nginx-{installed_nginx_version}.tar.gz")

# Extract NGINX source code
with tarfile.open(f"nginx-{installed_nginx_version}.tar.gz", "r:gz") as tar:
    tar.extractall()

# Compile ModSecurity dynamic module
os.chdir(f"nginx-{installed_nginx_version}")
subprocess.run(["./configure", "--with-compat", f"--add-dynamic-module=../ModSecurity-nginx"])
subprocess.run(["make", "modules"])

# Copy the module to the standard directory
shutil.copy("objs/ngx_http_modsecurity_module.so", "/etc/nginx/modules")

print("ModSecurity module compiled and copied to /etc/nginx/modules.")
