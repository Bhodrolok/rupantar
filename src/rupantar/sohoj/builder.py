from shutil import copytree, rmtree
from os import path, makedirs, chdir, getcwd
from glob import glob
import logging
import yaml
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

logger = logging.getLogger()


class Config:
    def __init__(self, config_file_path):
        # basic constructor for the class for instantiation
        # '_' variable = not intendeded to be used = throwaway value holder (in this case the filename without ext)
        _, extension = path.splitext(config_file_path)
        if extension == ".yaml" or extension == ".yml":
            try:
                with open(config_file_path, "r") as yaml_file:
                    config = yaml.safe_load(yaml_file)
                logger.info("Load configuration data from: %s", config_file_path)
            except OSError as err:
                logger.exception(
                    "Error reading and loading config data from %s: %s",
                    config_file_path,
                    str(err),
                )
        # TODO: Add TOML support
        else:
            logger.warning("Config file format: %s is not supported!", extension)

        # Dynamically set attributes to the instance for each key-value pair in the config file
        if config:
            for key, val in config.items():
                setattr(self, key, val)
                logger.debug("Setting attribute '%s' as: %s", key, val)
        else:
            logger.warning("Empty or invalid configuration. No attributes were set.")


def parse_md(md_file_path):
    try:
        with open(md_file_path) as infile:
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
        # Store file 'metadata', inside the front-matter, into post_detail
        post_detail = yaml.safe_load(ym_meta)
        logger.debug("Load post's metadata from: %s", md_file_path)
        # strip() to remove leading and trailing whitespace off of contents
        page_contents = md_contents.strip()
        logger.debug("Load post's page contents from: %s", md_file_path)

        return post_detail, page_contents
    except OSError as err:
        logger.exception(
            "Error loading metadata and page contents from %s: %s",
            md_file_path,
            str(err),
        )


def build_project(project_folder, config_file_name):
    # Create Page
    def create_page(page_template, post_detail, md, filename):
        just_filename = path.basename(filename)
        post_template = Environment(
            loader=FileSystemLoader(searchpath=project_folder)
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

    # Markdown file to string
    def md_to_str(md_file_path):
        with open(md_file_path) as data:
            return data.read()

    # Program entry
    try:
        # Change cwd to project folder
        chdir(project_folder)
        curr_dir = getcwd()
        logger.info(f"cwd is now: {curr_dir}")
        # Location of config file, assumed to be in abovementioned project folder
        config_file = "config.yml" if (config_file_name is None) else config_file_name
        config_file_path = path.join(config_file)
        project_folder = curr_dir
        # New Config object with data loaded from the config file
        config = Config(config_file_path)
        try:
            # Resource dir = Static assets (eg: static/); images, stylesheets, scrips, etc.
            resource_path_abs = path.join(project_folder, config.resource_path)
            # Home dir = Files to be served (eg: public/); web-accessible
            home_path_abs = path.join(project_folder, config.home_path)
            # Clear out existing public/ folder
            if path.exists(home_path_abs):
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

        # Sort posts based on date in descending order
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

    except Exception as err:
        logger.exception("Error: Failed to read %s: %s", config_file_path, str(err))

    else:
        print("Project built successfully.")
        logger.info("Project built at: %s", path.join(project_folder, config.home_path))
