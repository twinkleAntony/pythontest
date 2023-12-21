import os
import shutil
import subprocess
import tarfile
import urllib.request

def compile_modsecurity_nginx_connector():

    try:

        # Change the current working directory
        os.chdir(r"/usr/local/src/")

        # Verify that the program's working directory indeed changed
        print(f"The working directory is now '{os.getcwd()}'.")
        # Clone ModSecurity module
        subprocess.run([ "sudo","git", "clone", "--depth", "1", "https://github.com/SpiderLabs/ModSecurity-nginx.git"])
        # Determine NGINX version

        NGINX_VERSION =subprocess.check_output([ '`nginx -v 2>&1', '|',' awk {print $3}', '|', 'cut -d"/"', '-f', '2'])
        print("NGINX Version:", NGINX_VERSION)
        # Download NGINX source code
        nginx_url = "http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz"
        subprocess.run(['wget', nginx_url])

        subprocess.run(['tar', 'zxvf', 'nginx-$NGINX_VERSION.tar.gz'])
        os.chdir('nginx-$NGINX_VERSION;')

        # Compile the dynamic module

        subprocess.run(['./configure', '--with-compat', '--add-dynamic-module=../ModSecurity-nginx'])
        subprocess.run(['make', 'modules'])
        subprocess.run(["mkdir", "-p", "/etc/nginx/modules/"])
        print("Directory '/etc/nginx/modules/' created successfully.")
        subprocess.run(['cp', 'objs/ngx_http_modsecurity_module.so', '/etc/nginx/modules'])

        print("ModSecurity connector for NGINX compiled and installed successfully.")
    except Exception as e:
        print("Error during compilation: {e}")

if __name__ == "__main__":
    compile_modsecurity_nginx_connector()