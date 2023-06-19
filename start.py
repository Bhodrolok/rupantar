from argparse import ArgumentParser
from sohoj import creator, builder, server, __version__


def main():

    parser = ArgumentParser(prog='rupantar', description='Easily configurable static website generator with a focus on minimalism.')
    parser.add_argument("-v", "--version", action="version", version=f"{__version__}" )
    subparsers = parser.add_subparsers(dest='type', help='Supported commands', required=True)
    
    parser_init = subparsers.add_parser('init', help='Create new skeleton project at provided directory. Default config.')
    # TODO prompt for config fields into --> conf_data("{a}{b}").format(a=input1,b=input2)etc.
    parser_init.add_argument("mool", help="Name of project. Path relative to cwd.")

    parser_new = subparsers.add_parser('new', help="Create new post at provided rupantar project's content/note directory.")
    parser_new.add_argument("mool", help="Name of project directory. Path relative to cwd.")
    parser_new.add_argument("name", help="Filename of post without extension.")
    parser_new.add_argument("-sh", dest="show_home", help="If the post is to be shown in home page. Default True.", type=lambda x: x == 'True')
    
    parser_build = subparsers.add_parser('build', help='Build and generate static website pages from template and data. Default output directory is public/.')
    parser_build.add_argument("mool", help="Name of project directory. Path relative to cwd.")
    parser_build.add_argument("-c", "--config", nargs='?', help="Name of config file to use. Path relative to project directory. Default config.yml")

    parser_serve = subparsers.add_parser('serve', help='Start a local server for serving and previewing generated pages.')
    parser_serve.add_argument("mool", help="Name of project directory. Path relative to cwd.")
    parser_serve.add_argument("-c", "--config", nargs='?', help="Name of config file to use. Path relative to project directory. Default config.yml")
    parser_serve.add_argument("-p", "--port", help="Network port where the server will listen for requests. Default is random ephemeral port.", type=int)
    parser_serve.add_argument("-i", "--interface", help="Network interface to bind the server to. Default localhost/loopback interface")
    
    args = parser.parse_args()
    
    if args.type == "init" and args.mool:
        creator.createPidgey(args.mool)
    elif args.type == "new" and args.mool and args.name:
        creator.createNote(args.mool, args.name, args.show_home)
    elif args.type == 'build' and args.mool:
        builder.buildPidgey(args.mool, args.config)
    elif args.type == 'serve' and args.mool:
        server.start_server(args.mool, args.config, args.port, args.interface)
    
    else: 
        parser.print_help()

# Entry point
if __name__ == '__main__':
    main()

