import os
import subprocess
import urllib.request


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
        subprocess.run(['sudo', 'apt', 'install', 'libmodsecurity3'])

        print("libmodsecurity installed successfully.")

    except Exception as e:
        print(f"Error during ModSecurity installation: {e}")


def compile_modsecurity_nginx_connector():

    subprocess.run(['apt','install', 'build-essential'])
    # Change the current working directory
    os.chdir(r"/usr/local/src")
    # Verify that the program's working directory indeed changed
    print(f"The working directory is now '{os.getcwd()}'.")
    # Clone ModSecurity modulecd
    clone_directory = "/usr/local/src/ModSecurity-nginx"

    # Check if the directory already exists
    if os.path.exists(clone_directory):
        print("ModSecurity-nginx repository is already cloned.")

    else:
        # Clone ModSecurity module
        subprocess.run(
            ["sudo", "git", "clone", "--depth", "1", "https://github.com/SpiderLabs/ModSecurity-nginx.git",
             clone_directory])
        print("ModSecurity-nginx repository cloned successfully.")

    try:
        print('hi')
        nginx_version_cmd = "nginx -v 2>&1 | awk '{print $3}' | cut -d'/' -f 2"
        NGINX_VERSION = subprocess.check_output(nginx_version_cmd, shell=True, text=True).strip()
        print("NGINX Version:", NGINX_VERSION)

        # Download NGINX source code
        nginx_url = f"http://nginx.org/download/nginx-{NGINX_VERSION}.tar.gz"
        subprocess.run(['wget', nginx_url])
        try:
            with urllib.request.urlopen(nginx_url) as response, open(f"nginx-{NGINX_VERSION}.tar.gz", "wb") as outfile:
                outfile.write(response.read())
            print(f"Downloaded: nginx-{NGINX_VERSION}.tar.gz")
            subprocess.run(['tar', 'zxf', f"nginx-{NGINX_VERSION}.tar.gz"])
            os.chdir(f"nginx-{NGINX_VERSION}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"Error: NGINX version {NGINX_VERSION} not found on the server.")
            else:
                print(f"HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
        except Exception as e:
            print(f"Error: {e}")
            # Compile the dynamic module

        print(f"The working directory is now '{os.getcwd()}'.")
        configure_command = "./configure --add-dynamic-module=../ModSecurity-nginx --with-cc-opt='-g -O2 -ffile-prefix-map=/build/nginx-d8gVax/nginx-1.18.0=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security -fPIC -Wdate-time -D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro -Wl,-z,now -fPIC' --prefix=/usr/share/nginx --conf-path=/etc/nginx/nginx.conf --http-log-path=/var/log/nginx/access.log --error-log-path=/var/log/nginx/error.log --lock-path=/var/lock/nginx.lock --pid-path=/run/nginx.pid --modules-path=/usr/lib/nginx/modules --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-compat --with-debug --with-pcre-jit --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_auth_request_module --with-http_v2_module --with-http_dav_module --with-http_slice_module --with-threads --add-dynamic-module=/path/http-geoip2 --with-http_addition_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_sub_module"
        subprocess.run(configure_command, shell=True, check=True)

        # Run the 'make modules' command
        make_modules_command = "make modules"
        subprocess.run(make_modules_command, shell=True, check=True)

        subprocess.run(["mkdir", "-p", "/etc/nginx/modules/"])

        print(f"The working directory is now '{os.getcwd()}'.")
        subprocess.run(['cp', 'objs/ngx_http_modsecurity_module.so', '/etc/nginx/modules'])
        print("ModSecurity connector for NGINX compiled and installed successfully.")

    except Exception as e:
        print("Error during compilation: {e}")
#Python script to add load_module directive to NGINX configuration

config_path = "/etc/nginx/nginx.conf"
directive_to_add = 'load_module /etc/nginx/modules/ngx_http_modsecurity_module.so;'

def add_directive_to_config(config_path, directive):
    try:
        with open(config_path, 'r') as file:
            config_lines = file.readlines()

        # Check if the directive is already present
        if directive not in config_lines:
            # Add the directive to the end of the file
            config_lines.append(f"{directive}\n")

            # Write the modified content back to the file
            with open(config_path, 'w') as file:
                file.writelines(config_lines)

            print(f"Directive added to {config_path}")
        else:
            print(f"Directive already present in {config_path}")

    except FileNotFoundError:
        print(f"Error: {config_path} not found.")




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
            add_directive_to_config(config_path, directive_to_add)
        elif choice == '2':
            print('hi')

        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
