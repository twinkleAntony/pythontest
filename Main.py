import os
import subprocess
def install_required_packages():
    """
     # Install Prerequisite Packages
    - None
    """
    try:
        subprocess.run(['sudo', 'apt', 'update'])
        subprocess.run(['sudo', 'apt', 'upgrade'])

        subprocess.check_call([
            'apt-get', 'install', '-y', 'apt-utils', 'autoconf', 'automake',
            'build-essential', 'git', 'libcurl4-openssl-dev', 'libgeoip-dev',
            'liblmdb-dev', 'libpcre++-dev', 'libtool', 'libxml2-dev', 'libyajl-dev',
            'pkgconf', 'wget', 'zlib1g-dev'
        ])
        print("Successfully installed required packages.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing required packages: {e}")

# Call the function to install the packages

def install_modsecurity_nginx():
    try:
        subprocess.run(['sudo', 'apt', 'update'])
        # Install required packages for Nginx1

        subprocess.run(['sudo', 'apt', 'install', 'nginx'])
        print("Nginx with ModSecurity installed successfully.")
        # Install molecularity
        subprocess.run(['sudo', 'apt' ,'install ' ,'libmodsecurity3'])

        print("libmodsecurity installed successfully.")

    except Exception as e:
        print(f"Error during ModSecurity installation: {e}")


def compile_modsecurity_nginx_connector():

    try:

        # Change the current working directory
        os.chdir('/usr/local/src/')
        # Clone ModSecurity module
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/SpiderLabs/ModSecurity-nginx.git"])
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


def main():
    while True:
        print("\nModSecurity Installation Menu:")
        print("1. Install ModSec WAF")
        print("2. Secure the web application")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            install_required_packages()
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
