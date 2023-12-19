import subprocess


def compile_modsecurity_nginx_connector():
    try:
        # Clone the ModSecurity-nginx repository
        subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/SpiderLabs/ModSecurity-nginx.git'])

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

# Run the compilation function
compile_modsecurity_nginx_connector()
