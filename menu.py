import subprocess
def install_modsecurity_nginx():
    try:
        # Update the package list
        subprocess.run(['sudo', 'apt', 'update'])

        # Install required packages for Nginx
        subprocess.run(['sudo', 'apt', 'install', 'nginx', 'libnginx-mod-http-modsecurity'])

        # Enable the ModSecurity module
        subprocess.run(['sudo', 'ln', '-s', '/usr/share/modsecurity-crs/', '/etc/nginx/modsec'])

        # Include ModSecurity configuration in Nginx
        with open('/etc/nginx/nginx.conf', 'a') as conf_file:
            conf_file.write('\n')
            conf_file.write('include /etc/nginx/modsec/modsecurity.conf;')

        # Restart Nginx to apply changes
        subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])

        print("Nginx with ModSecurity installed successfully.")
    except Exception as e:
        print(f"Error during ModSecurity installation: {e}")
def main():
    while True:
        print("\nModSecurity Installation Menu:")
        print("1. Install ModSec WAF")
        print("2. Secure the web application")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            install_modsecurity_nginx()
        elif choice == '2':
            print('hi')

        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
