import os
import subprocess
import shutil
import urllib.request
import tarfile
import json

def get_latest_modsecurity_version():
    api_url = "https://api.github.com/repos/SpiderLabs/ModSecurity-nginx/releases/latest"
    with urllib.request.urlopen(api_url) as response:
        data = json.load(response)
        return data["tag_name"]

def download_compile_nginx_modsecurity_connector():
    try:
        # Get the latest ModSecurity-nginx version
        latest_version = get_latest_modsecurity_version()
        download_url = f"https://github.com/SpiderLabs/ModSecurity-nginx/archive/{latest_version}.tar.gz"
        download_dir = f"nginx_modsecurity_connector_{latest_version}"

        # Download and extract
        os.makedirs(download_dir, exist_ok=True)
        tar_filename = f"modsecurity-nginx-{latest_version}.tar.gz"
        tar_filepath = os.path.join(download_dir, tar_filename)
        urllib.request.urlretrieve(download_url, tar_filepath)

        with tarfile.open(tar_filepath, "r:gz") as tar:
            tar.extractall(path=download_dir)

        os.remove(tar_filepath)

        # Compile the module
        module_dir = os.path.join(download_dir, f"ModSecurity-nginx-{latest_version}")
        os.chdir(module_dir)

        # Check if the module directory already exists
        if os.path.exists("objs/ngx_http_modsecurity_module.so"):
            print(f"NGINX ModSecurity Connector {latest_version} has already been compiled.")
        else:
            subprocess.run(["./autogen.sh"])
            subprocess.run(["./configure"])
            subprocess.run(["make"])

            # Copy the compiled module
            nginx_modules_dir = "/etc/nginx/modules"
            shutil.copy("objs/ngx_http_modsecurity_module.so", nginx_modules_dir)

            print(f"NGINX ModSecurity Connector {latest_version} has been downloaded and compiled successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up: Remove the downloaded directory
        shutil.rmtree(download_dir, ignore_errors=True)

if __name__ == "__main__":
    download_compile_nginx_modsecurity_connector()
