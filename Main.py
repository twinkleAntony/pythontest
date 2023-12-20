import subprocess
import package

def install_modsecurity_nginx():
    try:
        subprocess.run(['sudo', 'apt', 'update'])
        # Install required packages for Nginx1
        subprocess.run(['sudo', 'apt', 'install', 'nginx'])
        # Install molecularity
        subprocess.run(['sudo', 'apt-get', 'install', 'libmodsecurity3'])

        print("libmodsecurity installed successfully.")

        # Include ModSecurity configuration in Nginx
       # with open('/etc/nginx/nginx.conf', 'a') as conf_file:
        #    conf_file.write('\n')
         #   conf_file.write('include /etc/nginx/modsec/modsecurity.conf;')

        # Restart Nginx to apply changes
        #subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])

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
