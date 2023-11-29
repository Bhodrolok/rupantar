from shutil import copytree, rmtree
from os import makedirs
from pathlib import Path
from logging import getLogger
from typing import Union
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown2 import markdown
from rupantar.sohoj.configger import Config
from rupantar.sohoj.utils import get_func_exec_time

logger = getLogger()


@get_func_exec_time
def parse_md(md_file_path: str) -> tuple[str, str]:
    """Parse a given Markdown file and extracts it's metadata and contents.

    Metadata = stuff enclosed within the front-matter ('---')
    Contents = Rest of the page contents, outside the front-matter

    Returns the metadata, as a dictionary, and the page contents, as a string.

    Args:
      md_file_path(str): The path to the markdown file

    Returns:
      tuple: A tuple containing the post's metadata and the page contents

    Raises:
      OSError: If any error opening or reading the markdown file

    """
    try:
        md_path = Path(md_file_path).resolve()
        with open(md_path) as infile:
            logger.info(f"Parsing file: {md_file_path}")
            yaml_lines, ym_meta, md_contents = [], "", ""

            for line in infile:
                if line.startswith("---"):
                    for line in infile:
                        if line.startswith("---"):
                            break
                        else:
                            yaml_lines.append(line)
                    # ym_meta = 'metadata' so stuff inside the --- ---
                    ym_meta = "".join(yaml_lines)
                    # md_contents = rest of page contents outside the --- ---
                    md_contents = "".join(infile)
                    break
        # Store file 'metadata', inside the front-matter, in post_detail
        post_detail = safe_load(ym_meta)
        logger.debug(f"Metadata: {post_detail}")
        # strip() to remove leading and trailing whitespace off of contents
        page_contents = md_contents.strip()
        logger.debug(f"Page contents: {page_contents}")

        return post_detail, page_contents

    except OSError as err:
        logger.exception(
            f"Error loading metadata and page contents from {md_file_path}\n {err}"
        )


@get_func_exec_time
def md_to_str(md_file_path: str) -> str:
    """Convert a given Markdown file to plain-text string.

    Args:
      md_file_path(str): The path to the markdown file

    Returns:
      string: A string containing the entire contents of the markdown file.

    Raises:
      OSError: If any error opening or reading the markdown file

    """
    # Possible TODO: Use a better(?) Markdown library for this
    try:
        md_path = Path(md_file_path).resolve()
        with open(md_path) as md_data:
            return md_data.read()

    except OSError as err:
        logger.exception(f"Error reading data from file: {md_file_path} :: {err}")


@get_func_exec_time
def build_project(project_folder: str, config_file_name: str) -> None:
    """Build a rupantar project, using an optional config file if provided.

    Generate the actual static site pages using data loaded from the config file.
    Store the output files in a public/ directory, within the rupantar project folder, ready to serve to clients at a web server.
    Overwrites existing public/ directory.

    Note:
        Applies Jinja2 templates in order to generate the static files.

    Args:
      project_folder (str): The name of an existing rupantar project.
      config_file_name (str): The name of the config file to load relevant project-specific configurations. Defaults to 'config.yml' that is created by creator.py when initializing a rupantar project.

    Raises:
      OSError: If any error opening or writing file
      FileNotFoundError: Missing rupantar project/config file

    """

    @get_func_exec_time
    def create_page(
        page_template: str, post_detail: dict, md: str, filename: str
    ) -> str:
        """Create a new HTML page from a given Jinja2 template and markdown content.

        Take a Jinja2 page template, post details, markdown content, and a filename,
        and create a new page with the given details. The new page will be saved to the same location as the original file.

        Args:
          page_template(str): The Jinja2 template to use for the new page
          post_detail(dict): The details of the post to include in the new page
          md(str): The markdown content to include in the new page
          filename(str): The name of the file to create

        Returns:
          str: The name of the new static file

        Raises:
          OSError: If any error opening or writing file

        """

        logger.debug(
            f"create_page() called with the following args:\npage_template = {page_template}\npost_detail = {post_detail}\nmd = {md}\nfilename = {filename}"
        )
        output_file = Path(filename).resolve()
        output_filename = output_file.name
        project_folder_path = Path(project_folder).resolve()
        page_template_path = Path(project_folder_path, page_template).resolve()
        template_search_path = page_template_path.parent.resolve()
        print(
            f"Creating page using Jinja template: {page_template}\nfrom: {page_template_path}"
        )
        post_template = Environment(
            loader=FileSystemLoader(searchpath=project_folder_path),
            autoescape=select_autoescape(["html", "htm", "xml"]),
        ).get_template(page_template)

        post_title = config.title
        post_date = (
            post_data
        ) = posts_list = last_date = nextpage = post_meta = post_subtitle = ""
        post_path = config.home_path

        if output_filename == "index.html":
            post_file = filename
            posts_list = posts
            post_path = Path(project_folder_path, config.home_path)

        elif output_filename.endswith(".html"):
            post_file = filename
            posts_list = posts
        elif output_filename.endswith(".xml"):
            post_file = filename
            posts_list = posts
            post_path = Path(project_folder_path, config.home_path)
            last_date = posts_list[0].get("date")
        elif post_detail is None:
            logger.info("Converting %s to .html format", output_file)
            post_file = filename.replace(".md", ".html")

        else:
            post_title = post_detail.get("title")
            post_subtitle = post_detail.get("subtitle")
            post_date = post_detail.get("date")
            post_meta = post_detail.get("meta")
            # post_data = filename.split('/')
            post_path = Path(project_folder, config.home_path)
            # post_file = post_data[2].replace('.md','.html')
            # Convert to HTML
            post_file = output_filename.replace(".md", ".html")
            # post_data = post_data[1]
            post_data = output_file.parent
            makedirs(post_path, exist_ok=True)

        # Define where new .html/.xml file will be located
        # Eg: public/file.html || public/file.xml
        post_file_new = Path(post_path, post_file).resolve()
        print(f"Creating: {post_file_new.name} @ {post_file_new}")
        with open(post_file_new, "w") as output_file:
            try:
                output_file.write(
                    post_template.render(
                        title=config.title,
                        post_title=post_title,
                        post_subtitle=post_subtitle,
                        date=post_date,
                        metad=post_meta,
                        url=Path(config.url, post_file),
                        article=markdown(md),
                        posts=posts_list,
                        home=config.home_md,
                        header=markdown(
                            md_to_str(Path(project_folder, config.header_md))
                        ),
                        footer=markdown(
                            md_to_str(Path(project_folder, config.footer_md))
                        ),
                        nextpage=nextpage,
                        last_date=last_date,
                        config=config.__dict__,
                    )
                )
                logger.info(f"Rendering and writing page: {post_file_new} complete")

            except OSError as err:
                logger.exception(
                    "Error rendering or writing to page %s: %s", post_file_new, str(err)
                )
        return post_file

    # Program entry
    try:
        config_file = "config.yml" if (config_file_name is None) else config_file_name
        # Get absolute paths for both the rupantar project and the config file (rather than keep 'em relative!)
        project_folder_path = Path(project_folder).resolve()
        logger.info(f"Rupantar project directory location: {project_folder_path}")
        config_file_path = Path(project_folder_path, config_file).resolve()
        logger.info(f"Config file location: {config_file_path}")
        # Instantiate Config object for reading and loading config data values
        config = Config(config_file_path)

        try:
            # Resource dir = Static assets (eg: static/); images, stylesheets, scrips, etc.
            resource_path_abs = Path(project_folder, config.resource_path).resolve()
            # Home dir = Files to be served (eg: public/); web-accessible
            home_path_abs = Path(project_folder, config.home_path).resolve()
            # Clear out existing public/ folder
            if Path.exists(home_path_abs):
                logger.warning("Found existing public/ folder. Removing it.")
                rmtree(home_path_abs)
            # Recreate home path with resource
            copytree(resource_path_abs, home_path_abs)
            logger.info(
                f"Finish copying static resources from {resource_path_abs}\n to output directory:  {home_path_abs}"
            )
        except OSError as err:
            logger.exception("Error: %s", str(err))

        # Create pages from content/notes/ all markdown files here...
        posts = []
        notes_path = Path(project_folder_path, config.content_path, "notes").resolve()
        print(f"Notes path is: {notes_path}")
        for each_note_md in Path(notes_path).glob("*.md"):
            print(f"Creating page using: {each_note_md}")
            post_detail, md = parse_md(each_note_md)
            # Create blog pages
            if post_detail is not None:
                post_url = create_page(
                    config.note_template, post_detail, md, each_note_md
                )
                ymd = post_detail
                ymd.update({"url": "/" + post_url})
                ymd.update({"note": markdown(md)})
                posts += [ymd]

        # Sort all blog posts based on date in a descending order
        posts = sorted(posts, key=lambda post: post["date"], reverse=True)

        # Create other pages using data in content/ (outside content/notes/)
        try:
            # home/
            home_content_path = Path(project_folder_path, config.home_md)
            home_page = create_page(
                config.home_template, None, md_to_str(home_content_path), "index.html"
            )
            logger.info(f"Home page created at:  {Path(home_page).resolve()}")
            # RSS feed
            # TODO: Check RSS content (.md)
            rss_feed = create_page(
                config.feed_template, None, md_to_str(home_content_path), "rss.xml"
            )
            logger.info(f"RSS feed created at:  {Path(rss_feed).resolve()}")
        except Exception as err:
            logger.exception("Error creating other pages: %s", str(err))

    except FileNotFoundError as err:
        logger.exception(f"{err}")

    except OSError as err:
        logger.exception(f"{err}")

    else:
        print(f"Project built successfully.")
        logger.info(
            f"rupantar Project built at: {Path(project_folder, config.home_path).resolve()}"
        )
