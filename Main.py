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
        subprocess.run(['noninteractive', 'get' ,'install', 'nginx-light'])

        print("Nginx with ModSecurity installed successfully.")
        # Install molecularity
        subprocess.run(['sudo', 'apt', 'install', 'libmodsecurity3'])
        subprocess.run(['sudo', 'apt', 'install', 'libmodsecurity-dev'])

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
        configure_command = "./configure --with-compat --add-dynamic-module=../ModSecurity-nginx"
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


def add_load_module_directive(config_path, directive):
    try:
        # Read the existing content of the file
        with open(config_path, 'r') as file:
            file_content = file.read()

        # Add the load_module directive to the beginning of the file
        new_content = f"{directive}\n{file_content}"

        # Write the modified content back to the file
        with open(config_path, 'w') as file:
            file.write(new_content)

        print(f"Load module directive added to the beginning of {config_path}")
    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Load module directive to be added
    load_module_directive = '# Instructs NGINX to load the ModSecurity dynamic module when it processes the configuration:\nload_module /etc/nginx/modules/ngx_http_modsecurity_module.so;'

    # File path to which the load module directive will be added
    nginx_config_path = "/etc/nginx/nginx.conf"  # Update this with the correct path

    try:
        # Add the load_module directive to the NGINX configuration file
        add_load_module_directive(nginx_config_path, load_module_directive)

        print(f"Load module directive added to {nginx_config_path}")
    except FileNotFoundError:
        print(f"Error: {nginx_config_path} not found.")
    except Exception as e:
        print(f"Error: {e}")
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
            add_load_module_directive()

        elif choice == '2':
            print('hi')

        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
