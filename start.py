from argparse import ArgumentParser
from sohoj import creator, builder, server, __version__


def main():

    parser = ArgumentParser(prog='rupantar', description='Easily configurable static website generator with a focus on minimalism.')
    parser.add_argument("-v", "--version", action="version", version="{version}".format(version=__version__) )
    subparsers = parser.add_subparsers(dest='type', help='supported commands', required=True)
    
    parser_init = subparsers.add_parser('init', help='Create new skeleton project at provided directory. Default config.')
    parser_init.add_argument("mool", help="Name of folder. Path relative to cwd.")

    parser_new = subparsers.add_parser('new', help='create new note/post/page')
    
    parser_build = subparsers.add_parser('build', help='build the pidgeotto')

    parser_serve = subparsers.add_parser('serve', help='serve the pidgeotto')
    
    args = parser.parse_args()
    
    if args.type == "init" and args.mool:
        creator.createPidgey(args.mool)
    elif args.type == "new" and args.name:
        creator.createNote(args.name)
    elif args.type == 'build':
        builder.buildPidgey()
    elif args.type == 'serve':
        server.server()
    
    else: 
        parser.print_help()

# Entry point
if __name__ == '__main__':
    main()

