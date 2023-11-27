from argparse import ArgumentParser
from rupantar.sohoj import builder, creator, logger, server
from rupantar import __version__


def main():
    parser = ArgumentParser(
        prog="rupantar",
        description="Easily configurable static website generator with a focus on minimalism.",
    )
    parser.add_argument("-v", "--version", action="version", version=f"{__version__}")
    parser.add_argument(
        "-l",
        "--log",
        dest="loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set logging level to control verbosity. Default INFO",
    )
    subparsers = parser.add_subparsers(
        dest="type", help="Supported commands", required=True
    )
    # as
    parser_init = subparsers.add_parser(
        "init", help="Create a new rupantar project at the given directory."
    )
    parser_init.add_argument(
        "mool",
        help="Name of project. A new directory with this name will be created in the current directory. ",
    )
    parser_init.add_argument(
        "-s",
        "--skip",
        action="store_true",
        help="Skip the prompts for selecting some config values. Can be updated by editing `config.yml` in the project directory.",
    )

    parser_new = subparsers.add_parser(
        "new",
        help="Create a new blog post at the given rupantar project's content/notes directory.",
    )
    parser_new.add_argument(
        "mool",
        help="Name of rupantar project. Path is relative to the current directory.",
    )
    parser_new.add_argument("name", help="New blog post filename (without extension).")
    parser_new.add_argument(
        "-sh",
        dest="show_home",
        help="If the post is to be shown in the home page. Default True.",
        type=lambda x: x == "True",
    )

    parser_build = subparsers.add_parser(
        "build",
        help="Build a rupantar project, generate the static pages. Deletes pre-existing output directory and creates a new one.",
    )
    parser_build.add_argument(
        "mool",
        help="Name of project directory. Path is relative to the current directory.",
    )
    parser_build.add_argument(
        "-c",
        "--config",
        nargs="?",
        help="Name of the config file to use. Path to this file is relative to the project directory. Default `config.yml`",
    )

    parser_serve = subparsers.add_parser(
        "serve",
        help="Start a local web server for serving and previewing generated pages.",
    )
    parser_serve.add_argument(
        "mool",
        help="Name of rupantar project. Path to this project is relative to the current directory.",
    )
    parser_serve.add_argument(
        "-c",
        "--config",
        nargs="?",
        help="Name of the config file to use. Path to this file is relative to the project directory. Default `config.yml`",
    )
    parser_serve.add_argument(
        "-p",
        "--port",
        help="Network port where the server will listen for requests. Default random ephemeral port (between 49152 and 65535).",
        type=int,
    )
    parser_serve.add_argument(
        "-i",
        "--interface",
        help="Network interface to bind the server to. Default localhost/loopback interface (127.0.0.1).",
    )

    args = parser.parse_args()

    # Configure logging, log level based on input
    logger.setup_logging(args.loglevel)

    if args.type == "init" and args.mool:
        # Interactive prompts for setting some default config.yml fields
        if args.skip:
            creator.create_project(args.mool, [None, None, None])
        else:
            print(
                "Hello there!\nPlease answer the following questions to set up your website's configuration!"
            )
            print(
                "This is completely optional and the questions can be skipped by leaving them blank."
            )
            print(
                "Choices can always be updated by modifying the `config.yml` file at project directory!"
            )
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
    elif args.type == "build" and args.mool:
        builder.build_project(args.mool, args.config)
    elif args.type == "serve" and args.mool:
        server.start_server(args.mool, args.config, args.port, args.interface)
    else:
        parser.print_help()


# Entry point
if __name__ == "__main__":
    main()
