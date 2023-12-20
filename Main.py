import os
import shutil
import subprocess
import tarfile
import urllib.request


def install_modsecurity_nginx():
    try:
        subprocess.run(['sudo', 'apt', 'update'])
        # Install required packages for Nginx1
        subprocess.run(['sudo', 'apt', 'install', 'nginx'])
        # Install molecularity
        subprocess.run(['sudo', 'apt-get', 'install', 'libmodsecurity3'])

        print("libmodsecurity installed successfully.")

        # Include ModSecurity configuration in Nginx
        with open('/etc/nginx/nginx.conf', 'a') as conf_file:
            conf_file.write('\n')
        conf_file.write('include /etc/nginx/modsec/modsecurity.conf;')

        # Restart Nginx to apply changes
        #subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])

        print("Nginx with ModSecurity installed successfully.")

    except Exception as e:
        print(f"Error during ModSecurity installation: {e}")


def compile_modsecurity_nginx_connector(version="v0.1.0"):
    download_url = f"https://github.com/SpiderLabs/ModSecurity-nginx/releases/download/{version}/modsecurity-nginx-{version}.tar.gz"
    download_dir = f"nginx_modsecurity_connector_{version}"

    try:
        # Download and extract
        os.makedirs(download_dir, exist_ok=True)
        tar_filename = f"modsecurity-nginx-{version}.tar.gz"
        tar_filepath = os.path.join(download_dir, tar_filename)
        urllib.request.urlretrieve(download_url, tar_filepath)

        with tarfile.open(tar_filepath, "r:gz") as tar:
            tar.extractall(download_dir)

        os.remove(tar_filepath)

        # Compile the module
        module_dir = os.path.join(download_dir, f"modsecurity-nginx-{version}")
        os.chdir(module_dir)

        subprocess.run(["./configure"])
        subprocess.run(["make"])

        # Copy the compiled module
        nginx_modules_dir = "/etc/nginx/modules"
        shutil.copy("objs/ngx_http_modsecurity_module.so", nginx_modules_dir)

        print(f"NGINX ModSecurity Connector {version} has been downloaded and compiled successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up: Remove the downloaded directory
        shutil.rmtree(download_dir, ignore_errors=True)





def main():
    while True:
        print("\nModSecurity Installation Menu:")
        print("1. Install ModSec WAF")
        print("2. Secure the web application")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            install_modsecurity_nginx()
            compile_modsecurity_nginx_connector()





        elif choice == '2':
            print('hi')

        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
