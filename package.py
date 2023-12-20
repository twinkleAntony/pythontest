import subprocess

def install_packages(package_list):
    """
    Install a list of packages using apt-get.

    Parameters:
    - package_list: A list of package names to install.

    Returns:
    - None
    """
    try:
        subprocess.run(['sudo', 'apt', 'update'])
        subprocess.run(['sudo', 'apt', 'upgrade'])
        # Construct the apt-get install command with the package names
        install_command = ['sudo', 'apt-get', 'install', '-y'] + package_list
        subprocess.check_call(install_command)
        print(f"Successfully installed packages: {', '.join(package_list)}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")

# List of packages to install
packages_to_install = [
     'git' 'apt-utils', 'autoconf', 'automake', 'build-essential', 'git',
    'libcurl4-openssl-dev', 'libgeoip-dev', 'liblmdb-dev', 'libpcre++-dev',
    'libtool', 'libxml2-dev', 'libyajl-dev', 'pkgconf', 'wget', 'zlib1g-dev'
]

# Call the function to install the packages
install_packages(packages_to_install)
