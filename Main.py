import subprocess


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


def compile_modsecurity_nginx_connector():

    try:
        # Clone the ModSecurity-nginx repository
        subprocess.run(['sudo', 'git', 'clone', '--depth', '1', 'https://github.com/SpiderLabs/ModSecurity-nginx.git'])

        # Determine NGINX version
        nginx_version_process = subprocess.run(['nginx', '-v'], capture_output=True, text=True)
        nginx_version = nginx_version_process.stdout.split('/')[1].strip()

        # Download NGINX source code
        nginx_source_url = f'http://nginx.org/download/nginx-{nginx_version}.tar.gz'
        subprocess.run(['wget', nginx_source_url])
        subprocess.run(['tar', 'zxvf', f'nginx-{nginx_version}.tar.gz'])

        # Compile the dynamic module
        subprocess.run(['cd', f'nginx-{nginx_version}'])
        subprocess.run(['./configure', '--with-compat', f'--add-dynamic-module=../ModSecurity-nginx'])
        subprocess.run(['make', 'modules'])
        subprocess.run(['cp', 'objs/ngx_http_modsecurity_module.so', '/etc/nginx/modules'])

        print("ModSecurity connector for NGINX compiled and installed successfully.")
    except Exception as e:
        print(f"Error during compilation: {e}")
    finally:
        # Clean up: Remove the cloned repositories and downloaded files
        subprocess.run(['rm', '-rf', 'ModSecurity-nginx', f'nginx-{nginx_version}', f'nginx-{nginx_version}.tar.gz'])






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
