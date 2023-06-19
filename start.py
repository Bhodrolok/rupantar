from argparse import ArgumentParser
from sohoj import creator, builder, server, __version__


def main():

    parser = ArgumentParser(prog='rupantar', description='Easily configurable static website generator with a focus on minimalism.')
    parser.add_argument("-v", "--version", action="version", version=f"{__version__}" )
    subparsers = parser.add_subparsers(dest='type', help='supported commands', required=True)
    
    parser_init = subparsers.add_parser('init', help='Create new skeleton project at provided directory. Default config.')
    parser_init.add_argument("mool", help="Name of directory. Path relative to cwd.")

    parser_new = subparsers.add_parser('new', help="Create new post at provided rupantar project's content/note directory.")
    parser_new.add_argument("mool", help="Name of project directory. Path relative to cwd.")
    parser_new.add_argument("name", help="Filename of post without extension.")
    parser_new.add_argument("-sh", dest="show_home", help="If the post is to be shown in home page. Default True.", type=lambda x: x == 'True')
    
    parser_build = subparsers.add_parser('build', help='build the pidgeotto')

    parser_serve = subparsers.add_parser('serve', help='serve the pidgeotto')
    
    args = parser.parse_args()
    
    if args.type == "init" and args.mool:
        creator.createPidgey(args.mool)
    elif args.type == "new" and args.mool and args.name:
        creator.createNote(args.mool, args.name, args.show_home)
    elif args.type == 'build':
        builder.buildPidgey()
    elif args.type == 'serve':
        server.server()
    
    else: 
        parser.print_help()

# Entry point
if __name__ == '__main__':
    main()

