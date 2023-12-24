from __future__ import annotations
from dataclasses import dataclass
from shutil import copytree, rmtree
from os import makedirs
from pathlib import Path
from logging import getLogger
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown2 import markdown
from rupantar.sohoj.configger import Config
from rupantar.sohoj.utils import get_func_exec_time, resolve_path

logger = getLogger()


# https://docs.python.org/3/library/dataclasses.html#module-dataclasses
@dataclass(slots=True)
class ProjectData:
    """Store configuration data for a rupantar project.

    Attributes:
        project_name (str): Name of rupantar project. Relative path.
        config (Config): The rupantar config object.
    """

    project_name: str
    config: Config


@dataclass(slots=True)
class PageData:
    """Store configuration data for rendering and creating a static page.

    Attributes:
        page_template (str): The Jinja2 template to use for rendering this page.
        posts (list[str]): The list of posts to include in the new page.
        page_metadata (dict[str]): The front matter-based details to be included. Eg: title, description, etc.
        md_content (str): The content of the page, in markdown.
        out_filename (str): The name of the file to create i.e. new page name.
    """

    page_template: str
    posts: list[str]
    page_metadata: dict[str]
    md_content: str
    out_filename: str


@get_func_exec_time
def parse_md(md_file_path: str) -> tuple[dict(str), str] | OSError | FileNotFoundError:
    """Parse a given Markdown file and extracts it's metadata and contents.

    Metadata is defined as whatever is enclosed within the front matter ('---'), in the top of the markdown file.
    Contents is defined as the rest of the page contents so to speak i.e. outside the front matter.

    Returns the metadata, as a dictionary, and the page contents, as a string.

    Note:
        The front matter format is that of YAML's key-value syntax, NOT MMD i.e. multi-markdown.

    Args:
      md_file_path(str): The path to the markdown file.

    Returns:
      tuple: A tuple containing the post's metadata and the page contents.

    Raises:
      OSError: If any error opening or reading the markdown file.
      FileNotFoundError: If the markdown file at the given path does not exist.

    """
    # TODO: Possibly look at: https://github.com/eyeseast/python-frontmatter ?
    try:
        md_path = resolve_path(md_file_path, strict=True)
        with open(md_path) as infile:
            logger.info(f"Parsing file: {md_file_path}")
            yaml_lines, ym_meta, md_contents = [], "", ""

            lines = iter(infile)
            for line in lines:
                if line.startswith("---"):
                    break

            for line in lines:
                if line.startswith("---"):
                    break
                yaml_lines.append(line)

            ym_meta = "".join(yaml_lines)
            md_contents = "".join(lines)

        post_detail = safe_load(ym_meta)
        logger.debug(f"Metadata: {post_detail}")
        # strip() to remove leading and trailing whitespace off of contents
        page_contents = md_contents.strip()
        logger.debug(f"Page contents: {page_contents}")
        return post_detail, page_contents

    except FileNotFoundError as err:
        logger.exception(f"Could not find markdown file: {md_file_path}\n {err}")

    except OSError as err:
        logger.exception(
            f"Error loading metadata and page contents from {md_file_path}\n {err}"
        )


@get_func_exec_time
def md_to_str(md_file: str) -> str:
    """Convert a given Markdown file to plain-text string.

    Args:
      md_file(str): The path to the markdown file.

    Returns:
      string: A string containing the entire contents of the markdown file.

    Raises:
      OSError: If any error opening or reading the markdown file.

    """
    try:
        md_path = resolve_path(md_file, strict=True)
        logger.debug(f"markdown file path: {md_path}")
        with open(md_path) as md_data:
            return md_data.read()

    except FileNotFoundError as err:
        logger.exception(f"Could not find markdown file: {md_file}\n {err}")

    except OSError as err:
        logger.exception(f"Error reading data from file: {md_file} :: {err}")


@get_func_exec_time
def create_page(
    project_data: ProjectData, page_data: PageData
) -> str | FileNotFoundError | OSError:
    """Create a new HTML page from a given Jinja2 template and markdown content.

    Take a Jinja2 page template, post details, markdown content, and a filename,
    and create a new page with the given details. The new page will be saved to the same location as the original file.

    Args:
        project_date (ProjectData): rupantar project config data
        page_data (PageData): page specific config data

    Returns:
        str: The name of the new static file.

    Raises:
        OSError: If any error opening or writing file.
        FileNotFoundError:

    """

    # logger.debug(inspect.signature(create_page))
    output_file = Path(page_data.out_filename)
    output_filename = output_file.name
    project_folder_path = resolve_path(project_data.project_name, strict=True)
    page_template_path = resolve_path(
        project_folder_path, page_data.page_template, strict=True
    )
    logger.info(
        f"Building page using template: {page_data.page_template} from: {page_template_path}"
    )
    rd_page_template = Environment(
        loader=FileSystemLoader(searchpath=project_folder_path),
        autoescape=select_autoescape(["html", "htm", "xml"]),
    ).get_template(page_data.page_template)

    page_header = project_data.config.title
    post_date = (
        post_data
    ) = posts_list = last_date = next_page = post_meta = page_subtitle = post_file = ""
    page_out_path = project_data.config.home_path

    if output_filename == "index.html":
        post_file = page_data.out_filename
        posts_list = page_data.posts
        page_out_path = Path(project_folder_path, project_data.config.home_path)
    elif output_filename.endswith(".html"):
        post_file = page_data.out_filename
        posts_list = page_data.posts
    elif output_filename.endswith(".xml"):
        post_file = page_data.out_filename
        posts_list = page_data.posts
        page_out_path = Path(project_folder_path, project_data.config.home_path)
        last_date = posts_list[0].get("date")
    elif page_data.page_metadata is None:
        logger.info(f"Converting {output_file} to .html format")
        post_file = output_filename.replace(".md", ".html")

    else:
        page_header = page_data.page_metadata.get("title")
        page_subtitle = page_data.page_metadata.get("subtitle")  # Optional
        post_date = page_data.page_metadata.get("date")
        post_meta = page_data.page_metadata.get("meta")  # XD
        # post_data = filename.split('/')
        page_out_path = Path(
            project_folder_path, project_data.config.home_path
        )  # Don't resolve just yet
        # post_file = post_data[2].replace('.md','.html')
        # Convert to HTML
        post_file = output_filename.replace(".md", ".html")
        # post_data = post_data[1]
        post_data = output_file.parent
        makedirs(page_out_path, exist_ok=True)

    # Define where new .html/.xml file will be located
    # Eg: public/file.html || public/file.xml, 'public' dir from 'config.home_path' value
    logger.debug(f"Post data: {post_data}")
    post_file_new = resolve_path(page_out_path, post_file)
    logger.info(f"Creating: {post_file_new.name} at: {post_file_new}")
    with open(post_file_new, "w") as output_file:
        try:
            output_file.write(
                rd_page_template.render(
                    config=project_data.config.__dict__,
                    title=page_header,
                    page_title=project_data.config.site_title,
                    page_desc=page_subtitle,
                    date=post_date,
                    metad=post_meta,
                    url=Path(project_data.config.url, post_file),
                    article=markdown(page_data.md_content),
                    posts=posts_list,
                    home=project_data.config.home_md,
                    header=markdown(
                        md_to_str(
                            Path(project_folder_path, project_data.config.header_md)
                        )
                    ),
                    footer=markdown(
                        md_to_str(
                            Path(project_folder_path, project_data.config.footer_md)
                        )
                    ),
                    nextpage=next_page,
                    last_date=last_date,
                )
            )
            logger.info(f"Rendering and writing page: {post_file_new} complete")

        except OSError as err:
            logger.exception(
                "Error rendering or writing to page %s: %s", post_file_new, str(err)
            )

    return post_file


@get_func_exec_time
def build_project(
    project_folder: str, config_file_name: str | None
) -> None | FileNotFoundError:
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

    try:
        print("Building project...")
        # Get absolute paths for both the rupantar project and the config file (rather than keep 'em relative!)
        project_folder_path = resolve_path(project_folder, strict=True)
        logger.info(f"Rupantar project directory location: {project_folder_path}")
        # Default values for config here instead of directly on function signature
        config_file = "config.yml" if (config_file_name is None) else config_file_name
        config_file_path = resolve_path(project_folder_path, config_file, strict=True)
        logger.info(f"Config file location: {config_file_path}")
        # Instantiate Config object for reading and loading config data values
        config = Config(config_file_path)

        project_data = ProjectData(project_folder_path, config)

        # Resource dir = Static assets (eg: static/); images, stylesheets, scrips, etc.
        resource_path_abs = resolve_path(
            project_folder, config.resource_path, strict=True
        )
        # Home dir = Files to be served (eg: public/); web-accessible (NOT created at this point)
        home_path_abs = resolve_path(project_folder, config.home_path)
        # Clear out existing public/ folder
        if Path.exists(home_path_abs):
            logger.info("Found existing public/ folder. Removing it.")
            rmtree(home_path_abs)
        # Recreate home path with resource
        copytree(resource_path_abs, home_path_abs)
        logger.info(
            f"Finish copying static resources from {resource_path_abs}\n to output directory:  {home_path_abs}"
        )

        posts = []

        # Build the pages from markdown content based out of content/notes/*.md
        notes_path = resolve_path(
            project_folder_path, config.content_path, "notes", strict=True
        )
        logger.info(f"Notes path: {notes_path}")
        for each_note_md in Path(notes_path).glob("*.md"):
            logger.info(f"Creating page using: {each_note_md}")
            post_detail, md_content = parse_md(each_note_md)
            # Create blog pages
            if post_detail is not None:
                page_data_posts = PageData(
                    config.note_template, posts, post_detail, md_content, each_note_md
                )
                post_url = create_page(project_data, page_data_posts)
                ymd = post_detail
                ymd.update({"url": "/" + post_url})
                ymd.update({"note": markdown(md_content)})
                posts += [ymd]

        # Sort all blog posts based on date in a descending order
        posts = sorted(posts, key=lambda post: post["date"], reverse=True)

        # Create the other pages from data in content directory
        home_content_path = Path(project_folder_path, config.home_md)
        page_data_home = PageData(
            config.home_template, posts, None, md_to_str(home_content_path), "index.html"
        )
        home_page = create_page(project_data, page_data_home)
        logger.info(f"Home page created at:  {resolve_path(home_page)}")

        page_data_rss = PageData(
            config.feed_template, posts, None, md_to_str(home_content_path), "rss.xml"
        )
        # TODO: Check RSS content
        rss_feed = create_page(project_data, page_data_rss)
        logger.info(f"RSS feed created at:  {resolve_path(rss_feed)}")
        # Finish
        print("Project built successfully.")
        logger.info(
            f"rupantar Project built at: {resolve_path(project_folder, config.home_path)}"
        )

    except FileNotFoundError as err:
        logger.exception("Error: %s", str(err))

    except OSError as err:
        logger.exception("Error: %s", str(err))
