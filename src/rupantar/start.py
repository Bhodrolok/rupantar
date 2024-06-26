from rupantar import __version__
from rupantar.sohoj import builder, creator, logger, server_watcher, utils
from xdg_base_dirs import xdg_data_home
import typer
from typing_extensions import Annotated
from typing import Optional
from rich import print

LOGS_LOCATION = f"{xdg_data_home()}\\rupantar\\logs"

app = typer.Typer(
    name="rupantar", 
    help="Simple configurable static website generator with a focus on minimalism.",
    rich_markup_mode="markdown"
    )

def version_callback(value: bool):
    if value:
        print(f"rupantar version: {__version__}")
        raise typer.Exit()

def log_location_callback(value: bool):
    if value:
        print(f"Logs are stored here: {LOGS_LOCATION}")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", "-V",
            callback=version_callback,
            is_eager=True, 
            help="Show the *version* and exit." 
            ),
        ] = None,
    verbosity: Annotated[
        int,
        typer.Option(
            "--verbose", "-v",
            count=True,
            help="Set the level of verbosity of **output** on the **console** :computer:. `-vvv` is max verbosity, followed by `-vv` and then `-v`."   
            ),
        ] = 0,
    log_location: Annotated[
        Optional[bool],
        typer.Option(
            "--logs", "-l",
            callback=log_location_callback,
            help="Show the location of the logs directory and exit."
            ),
        ] = None,
    log_to_console: Annotated[
        bool,
        typer.Option(
            "--log-to-console", "-l2c",
            help="Display the app logs to console. Off by default.",
            is_flag=True,
        ),
    ] = False,
    ):
    # Configure logging and instantiate the root logger
    logger.setup_logging(logger_name=__name__, log_to_console=log_to_console)
    utils.set_verbosity(verbosity)

@app.command("init")
def init_project(
    project: Annotated[
        str, 
        typer.Argument(help="Name of your project.", show_default=False)
        ],
    skip: Annotated[
        bool,
        typer.Option(
            "--skip", "-s",
            help="Skip asking for prompts for setting up some config values for the project. Can be updated by editing `config.yml` in the project's root directory.",
            show_default="Doesn't skip!",
            is_flag=True
            ),
    ] = False, 
    ):
    """
    Create a new skeleton rupantar project.

    This command will create a (sub-)directory, with the provided name, in the current working directory.
    """

    if skip:
        creator.create_project(project, [None, None, None])
    else:
        print(
                "Hello there!\nPlease answer the following questions to set up your website's configuration!"
        )
        print(
            "This is a completely optional step and the questions can be skipped by simply leaving them blank."
        )
        print(
            "Choices can always be updated by modifying the `config.yml` file in the project directory. Happy hacking!"
        )
        user_prompts = []
        site_url = typer.prompt("Site URL", default="your.domain.tld")
        user_prompts.append(site_url)
        site_desc = typer.prompt("Site description i.e. content in the HTML <meta> tag", default="Very cool webpage with a lot of content")
        user_prompts.append(site_desc)
        need_custom = typer.prompt("Do you want to add any custom templates? (Y/N)", default="N")
        user_prompts.append(need_custom)
        creator.create_project(project, user_prompts)

@app.command("new")
def add_new_page(
    project: Annotated[
        str, 
        typer.Argument(help="Name of rupantar project.", show_default=False)
        ], 
    name: Annotated[
        str, 
        typer.Argument(help="New post filename (without extension).", show_default=False)
        ],
    show_home: Annotated[
        bool,
        typer.Option(
            "--show-home", "-sh",
            help="If new page is to be shown in the home page. New posts are not shown in the home page by default.",    
            is_flag=True
            ),
        ] = False,
    ):
    """
    Create a new blog post.
    
    This command will create a new post in the given rupantar project's content/notes directory.
    """

    creator.create_note(project, name, show_home)

@app.command("build")
def build_site(
    project: Annotated[
        str, 
        typer.Argument(help="Name of rupantar project. Path relative to the current directory.", show_default=False),
        ],
    config: Annotated[
        str, 
        typer.Option(
            "--config", "-c",
            help="Path to the config file, relative to project directory. Defaults to `config.yml` in the project's root directory.",
            ),
        ] = None,
    ):
    """
    Build a rupantar project.

    This command generates the static pages for your website and stores them in the output directory.
    It also deletes any pre-existing output directory and creates a new one.
    The site is then ready for deployment to a static hosting service such as GitHub Pages (or your own hardware!).
    
    """

    builder.build_project(project, config)

@app.command("serve")
def serve_site(
    project: Annotated[
        str, 
        typer.Argument(help="Name of rupantar project.", show_default=False)
        ],
    port: Annotated[
        int,
        typer.Option(
            "--port", "-p",
            help="Network port where the server will listen for requests. Default random ephemeral port (between 49152 and 65535).",
            ),
        ] = None,
    config: Annotated[
        str, 
        typer.Option(
            "--config", "-c",
            help="Path to the config file, relative to project directory. Defaults to `config.yml` in the project's root directory.",
            ),
        ] = None,
    interface: Annotated[
        str,
        typer.Option(
            "--interface", "-i",
            help="Network interface to bind the server to. Defaults to the localhost/loopback interface.",
            ),
        ] = "127.0.0.1",
    open: Annotated[
        bool,
        typer.Option(
            "--open", "-o",
            help="Open the generated site in the default browser. Tries to do so in a new tab if a browser window's already open. Defaults to False.",
            ),
        ] = False,
    ):
    """
    Start a local web server for serving and previewing generated pages of your website.
    """

    server_watcher.start_watchful_server(project, config, port, interface, open)

if __name__ == "__main__":
    app()