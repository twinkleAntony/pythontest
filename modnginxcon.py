import os
import subprocess
import shutil
import urllib.request
import tarfile

def download_compile_nginx_modsecurity_connector():
    download_url =  subprocess.run(['sudo', 'git', 'clone', '--depth', '1', 'https://github.com/SpiderLabs/ModSecurity-nginx.git'])
    download_dir = subprocess.run(['nginx', '-v'])
    try:
        # Download and extract
        os.makedirs(download_dir, exist_ok=True)
        tar_filename = f"modsecurity-nginx-{version}.tar.gz"
        tar_filepath = os.path.join(download_dir, tar_filename)
        urllib.request.urlretrieve(download_url, tar_filepath)

        with tarfile.open(tar_filepath, "r:gz") as tar:
            tar.extractall(path=download_dir)

        os.remove(tar_filepath)

        # Compile the module
        module_dir = os.path.join(download_dir, f"ModSecurity-nginx-{version}")
        os.chdir(module_dir)

        subprocess.run(["./configure"])
        subprocess.run(["make"])

        # Copy the compiled module
        nginx_modules_dir = "/etc/nginx/modules"
        shutil.copy("objs/ngx_http_modsecurity_module.so", nginx_modules_dir)

        print(f"NGINX ModSecurity Connector {version} has been downloaded and compiled successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
      

if __name__ == "__main__":
    download_compile_nginx_modsecurity_connector()
