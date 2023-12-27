import os
import subprocess
import urllib.request
import re


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
        subprocess.run(['sudo', 'get' ,'install', 'nginx'])

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
def add_load_module_directive():
    directive ='load_module /etc/nginx/modules/ngx_http_modsecurity_module.so;'

    # File path to which the load module directive will be added
    config_path = "/etc/nginx/nginx.conf"  # Update this with the correct path

    try:
        # Read the existing content of the file
        with open(config_path, 'r') as file:
            lines = file.readlines()

        # Insert the load_module directive as the second line
        lines.insert(3, f"{directive}\n")
        lines.append(f"{directive}\n")
        # Write the modified content back to the file
        with open(config_path, 'w') as file:
            file.writelines(lines)

        print(f"Load module directive added to the second line of {config_path}")
    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
    except Exception as e:
        print(f"Error: {e}")



def download_and_setup_modsecurity_config():
    try:
        modsec_config_dir = "/etc/nginx/modsec"
        modsec_config_url = "https://raw.githubusercontent.com/SpiderLabs/ModSecurity/v3/master/modsecurity.conf-recommended"
        unicode_mapping_url = "https://raw.githubusercontent.com/SpiderLabs/ModSecurity/master/unicode.mapping"
        tmp_dir = "/tmp"

        # Create modsec directory
        subprocess.run(["mkdir", "-p", modsec_config_dir], check=True)

        # Download and move modsecurity.conf file
        subprocess.run(["wget", "-P", modsec_config_dir, modsec_config_url], check=True)
        subprocess.run(["mv", f"{modsec_config_dir}/modsecurity.conf-recommended", f"{modsec_config_dir}/modsecurity.conf"], check=True)

        # Download unicode mapping file
        os.chdir(r"/tmp")
        subprocess.run(["wget", "-c", unicode_mapping_url], check=True)
        subprocess.run(["cp", "-v", f"{tmp_dir}/unicode.mapping", f"{modsec_config_dir}/"], check=True)

        print("ModSecurity configuration files downloaded and set up successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
def change_sec_rule_engine():
    try:
        modsec_config_file = "/etc/nginx/modsec/modsecurity.conf"

        # Use sed to replace SecRuleEngine directive in the ModSecurity configuration file
        subprocess.run(["sed", "-i", 's/SecRuleEngine DetectionOnly/SecRuleEngine On/', modsec_config_file], check=True)

        print("SecRuleEngine directive changed to 'On' in the ModSecurity configuration file.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
def is_content_present(config_content, content_to_check):
    return re.search(re.escape(content_to_check), config_content, flags=re.DOTALL) is not None

def configure_nginx_with_modsecurity():
    nginx_config_path = "/etc/nginx/sites-enabled/default"
    modsec_rules_file = "/etc/nginx/modsec/main.conf"
    try:
        with open(nginx_config_path, 'r') as file:
            nginx_config_content = file.read()

        # Specify the content to add
        new_content = f'''
            modsecurity on;
            modsecurity_rules_file {modsec_rules_file};
         
        '''
        # Check if the content is already present inside the server block
        if not is_content_present(nginx_config_content, new_content):
            # Find the first occurrence of '}' after 'server {' and add the new content before it
            updated_config = re.sub(r'server {([^}]*})', fr'server {{{new_content}\1', nginx_config_content,
                                    flags=re.DOTALL)

            with open(nginx_config_path, 'w') as file:
                file.write(updated_config)

            print("ModSecurity directives added to the NGINX configuration file.")
        else:
            print("Content is already present. No modification needed.")
        # Find the first occurrence of '}' after 'server {' and add the new content before it


        print("ModSecurity directives and proxy_pass added to the NGINX configuration file.")
    except FileNotFoundError:
        print(f"Error: {nginx_config_path} not found.")
    except Exception as e:
        print(f"Error: {e}")


def edit_main_conf():
    main_conf_path = "/etc/nginx/modsec/main.conf"

    try:
        with open(main_conf_path, 'a') as file:
            # Add or modify the content
            file.write('\n')
            file.write('Include "/etc/nginx/modsec/modsecurity.conf"\n')
            file.write('\n# OWASP CRS setup\n')
            file.write('Include /etc/nginx/modsec/owasp-modsecurity-crs/crs-setup.conf\n')
            file.write('Include /etc/nginx/modsec/owasp-modsecurity-crs/plugins/*-config.conf\n')
            file.write('Include /etc/nginx/modsec/owasp-modsecurity-crs/plugins/*-before.conf\n')
            file.write('Include /etc/nginx/modsec/owasp-modsecurity-crs/rules/*.conf\n')
            file.write('Include /etc/nginx/modsec/owasp-modsecurity-crs/plugins/*-after.conf\n')

        print("Modifications added to main.conf successfully.")
    except FileNotFoundError:
        print(f"Error: {main_conf_path} not found.")
    except Exception as e:
        print(f"Error: {e}")


def check_if_owasp_crs_exists():
    owasp_crs_dir = "/etc/nginx/modsec/owasp-modsecurity-crs"
    return os.path.exists(owasp_crs_dir) and os.listdir(owasp_crs_dir)

def setup_owasp_crs():
    try:
        modsec_dir = "/etc/nginx/modsec"
        owasp_crs_repo = "https://github.com/coreruleset/coreruleset"
        owasp_crs_dir = "owasp-modsecurity-crs"

        # Check if OWASP CRS already exists
        if check_if_owasp_crs_exists():
            print("OWASP CRS is already cloned. No need to clone again.")
            return

        # Clone OWASP CRS repository
        subprocess.run(["git", "clone", owasp_crs_repo], cwd=modsec_dir, check=True)

        # Create a symbolic link to the cloned repository
        subprocess.run(["ln", "-svf", "coreruleset", owasp_crs_dir], cwd=modsec_dir, check=True)

        # Rename crs-setup.conf.example to crs-setup.conf
        subprocess.run(["mv", "-v", f"{owasp_crs_dir}/crs-setup.conf.example", f"{owasp_crs_dir}/crs-setup.conf"], cwd=modsec_dir, check=True)

        # Move and rename exclusion rule files
        subprocess.run(["mv", "-v", f"{owasp_crs_dir}/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example", f"{owasp_crs_dir}/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf"], cwd=modsec_dir, check=True)
        subprocess.run(["mv", "-v", f"{owasp_crs_dir}/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example", f"{owasp_crs_dir}/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf"], cwd=modsec_dir, check=True)

        print("OWASP CRS setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
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
            download_and_setup_modsecurity_config()
            change_sec_rule_engine()
            configure_nginx_with_modsecurity()
            edit_main_conf()
            setup_owasp_crs()

        elif choice == '2':
            print('hi')

        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
 main()
