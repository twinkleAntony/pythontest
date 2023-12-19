def modify_nginx_modsec_config(config_file_path, new_rules):
    try:
        # Open the configuration file in read mode ('r')
        with open(config_file_path, 'r') as file:
            # Read the content of the file
            content = file.read()

        # Modify the content (add or modify rules)
        # Here, we are just appending new rules to the end of the file
        content += '\n' + '\n'.join(new_rules)

        # Open the configuration file in write mode ('w') to overwrite the existing content
        with open(config_file_path, 'w') as file:
            # Write the modified content back to the file
            file.write(content)

        print(f'The file "{config_file_path}" has been successfully modified.')
    except FileNotFoundError:
        print(f'The file "{config_file_path}" does not exist.')
    except PermissionError:
        print(f'Permission error. Check if you have the necessary permissions to modify "{config_file_path}".')


# Example: Add new rules to the Nginx ModSecurity configuration file
nginx_modsec_config_path = '/etc/nginx/modsec/main.conf'
new_rules_to_add = [
    'SecRuleEngine On',
    'SecRequestBodyAccess On',
    # Add more rules as needed
]

modify_nginx_modsec_config(nginx_modsec_config_path, new_rules_to_add)
