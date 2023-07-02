from http.server import SimpleHTTPRequestHandler
from socket import SOL_SOCKET, SO_REUSEADDR
from socketserver import TCPServer
from os import path, chdir
import random
import ipaddress
import yaml

class Config:

    def __init__(self, config_file_path):

        # basic constructor for the class for instantiation
        # '_' variable = not intendeded to be used = throwaway value holder (in this case the filename without ext)
        _, extension = path.splitext(config_file_path)
        if extension == '.yaml' or extension == '.yml':
            try:
                with open(config_file_path, 'r') as yaml_file:
                    config = yaml.safe_load(yaml_file)
            except OSError as err:
                print(str(err))
        # TODO: Add TOML support
        else:
            print("Config file format: %s is not supported!", extension)

        # Dynamically set attributes to the instance for each key-value pair in the config file
        if config:
            for key, val in config.items():
                setattr(self, key, val)
        else:
            print("Empty or invalid configuration. No attributes were set.")

def validate_network_address(interface_address):
    #  validate the input to ensure a valid IP address
    # True = Valid, False = Invalid
    try:
        ip = ipaddress.ip_address(interface_address)
        # Invalid = NOT localhost OR 0.0.0.0
        if ip.is_link_local or ip.is_multicast:
            return False
        return True
    except ValueError:
        return False

def start_server(project_folder, config_file_name, port, interface_address):

    try:
        config_file = 'config.yml' if (config_file_name is None) else config_file_name
        # Ephemeral/dynamic/private ports, think good for temporary stuff 
        PORT = random.randint(49152, 65535) if ( (port is None) or (  ( port in range(0, 1024) ) ) ) else port
        HOST = interface_address if ( validate_network_address(interface_address) ) else '127.0.0.1'
        # Location of current file
        script_dir = path.dirname(path.dirname(path.abspath(__file__)))
        # Location of project folder with all contents
        project_folder_path = path.join(script_dir, project_folder)
        # Location of config file, assumed to be in abovementioned project folder
        config_file_path = path.join(project_folder_path, config_file)

        config = Config(config_file_path)
         # Change cwd to folder from where generated static filed will be served (public/ for example)  
        chdir(path.join(project_folder_path, config.home_path))
        try:
            with TCPServer((HOST, PORT), SimpleHTTPRequestHandler) as httpd:
                # Allow immediate socket re-use
                httpd.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                print(f"HTTP server listening @ http://{HOST}:{PORT}:")
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopping server...")
            httpd.server_close() 
    except:
        print("while serving pidgey, some issue occured.")
        print("This can be due to \n\t1. Not a pidgey directory. \n\t2. Pidgey not built yet.")
