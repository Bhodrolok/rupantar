from shutil import copytree, rmtree
from os import path, makedirs, chdir, getcwd
from glob import glob
import logging
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown2 import markdown
from rupantar.sohoj.configger import Config

logger = logging.getLogger()


def parse_md(md_file_path):
    """Parse a given Markdown file and extracts it's metadata and contents.

    Metadata = stuff enclosed within the front-matter ('---')
    Contents = Rest of page contents, for example the actual body of a post

    Returns the metadata, as a dictionary, and the page contents, as a string.

    Args:
      md_file_path(str): The path to the markdown file

    Returns:
      tuple: A tuple containing the post's metadata and the page contents

    Raises:
      OSError: If any error opening or reading the markdown file

    """
    try:
        with open(md_file_path) as infile:
            logger.debug(f".md file: {md_file_path}")
            yaml_lines, ym_meta, md_contents = [], "", ""

            for line in infile:
                if line.startswith("---"):
                    for line in infile:
                        if line.startswith("---"):
                            break
                        else:
                            yaml_lines.append(line)
                    # ym = 'metadata' so stuff inside the --- ---
                    ym_meta = "".join(yaml_lines)
                    # md = rest of page contents outside the --- ---
                    md_contents = "".join(infile)
                    break
        # Store file 'metadata', inside the front-matter, in post_detail
        post_detail = yaml.safe_load(ym_meta)
        logger.debug(f"Loaded post's metadata from: {md_file_path}")
        logger.debug(f"Metadata: {post_detail}")
        # strip() to remove leading and trailing whitespace off of contents
        page_contents = md_contents.strip()
        logger.debug(f"Page contents: {page_contents}")

        return post_detail, page_contents

    except OSError as err:
        logger.exception(
            f"Error loading metadata and page contents from {md_file_path}: {err}"
        )


def md_to_str(md_file_path):
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
        with open(md_file_path) as md_data:
            return md_data.read()

    except OSError as err:
        logger.exception(f"Error reading data from file: {md_file_path} :: {err}")


def build_project(project_folder, config_file_name):
    """Build a rupantar project, using an optional config file if provided.

    Generate the actual static site pages using data loaded from the config file.
    Store the output files in a public/ directory, within the rupantar project folder, ready to serve to clients at a web server.
    Overwrites existing public/ directory.

    Note:
        Applies Jinja2 templates in order to generate the static files.

    Args:
      project_folder: The name of an existing rupantar project.
      config_file_name(str): The name of the config file to load relevant project-specific configurations. Defaults to 'config.yml' that is created by creator.py when initializing a rupantar project.

    Raises:
      OSError: If any error opening or writing file
      FileNotFoundError: Missing rupantar project/config file

    """

    def create_page(page_template, post_detail, md, filename):
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
        just_filename = path.basename(filename)
        logger.info(f"Using template: {page_template} at {path.abspath(page_template)}")
        post_template = Environment(
            loader=FileSystemLoader(searchpath=project_folder),
            autoescape=select_autoescape(["html", "htm", "xml"]),
        ).get_template(page_template)
        post_title = config.title
        post_date = (
            post_data
        ) = posts_list = last_date = nextpage = post_meta = post_subtitle = ""
        post_path = config.home_path

        if just_filename == "index.html":
            post_file = filename
            posts_list = posts
        elif just_filename.endswith(".html"):
            post_file = filename
            posts_list = posts
        elif just_filename.endswith(".xml"):
            post_file = filename
            posts_list = posts
            last_date = posts_list[0].get("date")
        elif post_detail is None:
            logger.info("Converting %s to .html format", just_filename)
            post_file = filename.replace(".md", ".html")

        else:
            post_title = post_detail.get("title")
            post_subtitle = post_detail.get("subtitle")
            post_date = post_detail.get("date")
            post_meta = post_detail.get("meta")
            # post_data = filename.split('/')
            post_path = path.join(project_folder, config.home_path)
            # post_file = post_data[2].replace('.md','.html')
            # Convert to HTML
            post_file = path.basename(filename).replace(".md", ".html")
            # post_data = post_data[1]
            post_data = path.dirname(filename)
            makedirs(post_path, exist_ok=True)

        # Define where new .html/.xml file will be located
        # Eg: public/file.html || public/file.xml
        post_file_new = path.join(post_path, post_file)
        logger.info("Creating: %s", post_file_new)
        with open(post_file_new, "w") as output_file:
            try:
                output_file.write(
                    post_template.render(
                        title=config.title,
                        post_title=post_title,
                        post_subtitle=post_subtitle,
                        date=post_date,
                        metad=post_meta,
                        url=path.join(config.url, post_file),
                        article=markdown(md),
                        posts=posts_list,
                        home=config.home_md,
                        header=markdown(
                            md_to_str(path.join(project_folder, config.header_md))
                        ),
                        footer=markdown(
                            md_to_str(path.join(project_folder, config.footer_md))
                        ),
                        nextpage=nextpage,
                        last_date=last_date,
                        config=config.__dict__,
                    )
                )
                logger.info("Rendering and writing page: %s complete", post_file_new)

            except OSError as err:
                logger.exception(
                    "Error rendering or writing to page %s: %s", post_file_new, str(err)
                )

        return post_file

    # Program entry
    try:
        # Change cwd to the rupantar project folder
        chdir(project_folder)
        curr_dir = getcwd()
        logger.info(f"cwd is now: {curr_dir}")
        # Location of config file, assumed to be in abovementioned project folder
        config_file = "config.yml" if (config_file_name is None) else config_file_name
        config_file_path = path.join(config_file)
        project_folder = curr_dir
        logger.info(
            f"Config file path: {config_file_path}\nProject folder path: {project_folder}"
        )
        # New Config object with data loaded from the config file
        config = Config(config_file_path)
        try:
            # Resource dir = Static assets (eg: static/); images, stylesheets, scrips, etc.
            resource_path_abs = path.join(project_folder, config.resource_path)
            # Home dir = Files to be served (eg: public/); web-accessible
            home_path_abs = path.join(project_folder, config.home_path)
            # Clear out existing public/ folder
            if path.exists(home_path_abs):
                logger.warning("Found existing public/ folder. Removing it.")
                rmtree(home_path_abs)
            # Recreate home path with resource
            copytree(resource_path_abs, home_path_abs)
            logger.info("Finish copying: %s to %s", resource_path_abs, home_path_abs)
        except OSError as err:
            logger.info("Error: %s", str(err))

        # Create pages from content/notes/ all markdown files here...
        posts = []
        notes_path = path.join(config.content_path, "notes")
        for each_note_md in glob(path.join(notes_path, "*.md")):
            logger.debug(each_note_md)
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

        # Sort all blog pages/posts based on date in a descending order
        posts = sorted(posts, key=lambda post: post["date"], reverse=True)

        # Create other pages
        try:
            # home/
            create_page(
                config.home_template, None, md_to_str(config.home_md), "index.html"
            )
            # RSS
            create_page(
                config.feed_template, None, md_to_str(config.home_md), "rss.xml"
            )
        except Exception as err:
            logger.exception("Error creating other pages: %s", str(err))

    except FileNotFoundError:
        logger.exception(
            "Error: %s not found in %s directory. Make sure that both the file and directory exists.",
            config_file_path,
            project_folder,
        )

    except OSError as err:
        logger.exception("Error: Failed to read %s: %s", config_file_path, str(err))

    else:
        print("Project has been built successfully.")
        logger.info(
            f"rupantar Project built at: {path.join(project_folder, config.home_path)}"
        )
