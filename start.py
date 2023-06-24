from argparse import ArgumentParser
from os import mkdir, path
from datetime import datetime
import logging
from sohoj import creator, builder, server, __version__


def main():

    parser = ArgumentParser(prog='rupantar', description='Easily configurable static website generator with a focus on minimalism.')
    parser.add_argument("-v", "--version", action="version", version=f"{__version__}" )
    parser.add_argument("-l", "--log", dest="loglevel", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help="Set logging level to control verbosity. Default INFO")
    subparsers = parser.add_subparsers(dest='type', help='Supported commands', required=True)
    
    parser_init = subparsers.add_parser('init', help='Create new rupantar project skeleton at provided directory.')
    parser_init.add_argument("mool", help="Name of project. Path relative to cwd.")
    parser_init.add_argument("-s", "--skip", action="store_true", help="Skip prompts for choosing some config values. Can be updated by editing config.yml at project directory.")

    parser_new = subparsers.add_parser('new', help="Create new post at provided rupantar project's content/note directory.")
    parser_new.add_argument("mool", help="Name of project directory. Path relative to cwd.")
    parser_new.add_argument("name", help="Filename of post without extension.")
    parser_new.add_argument("-sh", dest="show_home", help="If the post is to be shown in home page. Default True.", type=lambda x: x == 'True')
    
    parser_build = subparsers.add_parser('build', help='Build rupantar project, generate static pages. Deletes pre-existing output directory and creates a new one.')
    parser_build.add_argument("mool", help="Name of project directory. Path relative to cwd.")
    parser_build.add_argument("-c", "--config", nargs='?', help="Name of config file to use. Path relative to project directory. Default config.yml")

    parser_serve = subparsers.add_parser('serve', help='Start a local server for serving and previewing generated pages.')
    parser_serve.add_argument("mool", help="Name of project directory. Path relative to cwd.")
    parser_serve.add_argument("-c", "--config", nargs='?', help="Name of config file to use. Path relative to project directory. Default config.yml")
    parser_serve.add_argument("-p", "--port", help="Network port where the server will listen for requests. Default random ephemeral port.", type=int)
    parser_serve.add_argument("-i", "--interface", help="Network interface to bind the server to. Default localhost/loopback interface.")
    
    args = parser.parse_args()

    # Configure logging
    # https://sematext.com/blog/python-logging/#basic-logging-configuration
    log_format_string_default = "%(asctime)s | [%(levelname)s] @ %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) => %(message)s"
    #logging.basicConfig(level=args.loglevel, format=log_formatter) # init root logger
    logger = logging.getLogger()  # root logger
    logger.setLevel(args.loglevel)

    if not path.exists('logs'):
        try:
            mkdir('logs')
        except OSError as err:
            logging.exception("%s", err)

    # Set handler for destination of logs, default to sys.stderr
    # Log destination = console
    logs_console_handler = logging.StreamHandler()
    logs_console_handler.setLevel(args.loglevel)
    #logger.addHandler(logs_console_handler)

    # Log destination = file
    log_filename = 'rupantar-' + datetime.now().strftime("%H-%M-%S_%p") + '.log'
    log_filepath = 'logs/' + log_filename
    logs_file_handler = logging.FileHandler(filename=log_filepath)
    # Create formatter object 
    file_handler_format = logging.Formatter(log_format_string_default)
    logs_file_handler.setFormatter(file_handler_format)
    logs_file_handler.setLevel(args.loglevel)
    # Assign handler to root logger
    logger.addHandler(logs_file_handler)
    
    if args.type == "init" and args.mool:
        # Interactive prompts for setting some default config.yml fields
        if args.skip:
            creator.create_project(args.mool, [None, None, None])
        else:
            print("Hello there!\nPlease answer the following questions to set up your website's configuration!")
            print("This is completely optional and the questions can be skipped by leaving them blank.")
            print("Choices can always be updated by modifying the `config.yml` file at project directory!")
            user_prompts = []
            site_url = input("Site URL? (yourdomain.tld): ")
            user_prompts.append(site_url)
            site_desc = input("Site description? : ")
            user_prompts.append(site_desc)
            need_custom = input("Do you want to add custom templates? (Y/N): ")
            user_prompts.append(need_custom)
            creator.create_project(args.mool, user_prompts)
    elif args.type == "new" and args.mool and args.name:
        creator.create_note(args.mool, args.name, args.show_home)
    elif args.type == 'build' and args.mool:
        builder.buildPidgey(args.mool, args.config)
    elif args.type == 'serve' and args.mool:
        server.start_server(args.mool, args.config, args.port, args.interface)
    
    else: 
        parser.print_help()

# Entry point
if __name__ == '__main__':
    main()

