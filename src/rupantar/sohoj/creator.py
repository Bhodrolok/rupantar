from pathlib import Path
from shutil import rmtree
from datetime import datetime
from logging import getLogger
from typing import Union
from rupantar.sohoj.utils import get_func_exec_time

# Use root logger = same instance from start.py [ https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial ]
# 'Child loggers propagate messages up to the handlers associated with their ancestor loggers.'
logger = getLogger()


def create_config(project_folder: Union[Path, str], user_choices: list[str]) -> None:
    """Create a configuration file for a rupantar project based on some user input.

    Expects the first param to be a project folder and the second to be a list of user choices.
    If the user skips providing any choices, default values will be used instead.
    Using these, a new 'config.yml' file is generated at the root of the rupantar project folder.
    The configuration file includes settings for the rupantar project (eg: site URL, templates, directories, and any other optional custom configurations).

    Args:
      project_folder(str or Path): The relative path to the project folder where the configuration file will be created
      user_choices(list of str): A list of user choices to set some configuration values

    Raises:
      OSError: If any error opening or writing to file

    """

    # Define the default values of the choices incase the user skips/provides blank input
    default_conf_values = [
        "yourdomain.tld",
        "Just another little corner on the interwebs.",
        "#",
    ]

    # Only set user prompts if they are NOT NONE + NOT JUST EMPTY SPACES (else no real validation done)
    url = (
        user_choices[0]
        if (user_choices[0] and user_choices[0].strip())
        else default_conf_values[0]
    )
    desc = (
        user_choices[1]
        if (user_choices[1] and user_choices[1].strip())
        else default_conf_values[1]
    )
    custom_needed = (
        ""
        if (user_choices[-1] and user_choices[-1].strip())
        else default_conf_values[-1]
    )
    try:
        config_file_path = Path(project_folder, "config.yml").resolve()
        logger.info(
            f"{config_file_path.name} file to be generated at: {config_file_path}"
        )
        with open(config_file_path, "w") as conf_file:
            conf_data = f"""# Required
title : Demo website    # Title in home/landing page (NOT the Page Title!)
url : {url}    # Site URL 

# Jinja templates
note_template : templates/note_template.html.jinja    # Blog posts i.e. notes page
home_template : templates/home_template.html.jinja    # Home page
feed_template : templates/feed_template.xml.jinja     # RSS feed
{custom_needed}custom_templates: 

# Directories
home_path : public      # Generated static files (served from here)
content_path : content  # Markdown files (define page contents and front-matter metadata)
resource_path : static  # Static assets (css, images, favicons, etc.) 

home_md : content/home.md       # Home page body
header_md : content/header.md   # Header
footer_md : content/footer.md   # Footer 

# Optional (Custom configs included here)
site-title : Demo Page Title                     
css : demo.css
desc : {desc}   # page description
mail : some@mail.com
"""
            conf_file.write(conf_data)
            logger.info(f"Created {config_file_path.name} at {config_file_path}")
    except OSError as err:
        logger.exception(f"Failed to create config.yml: {err}")


def create_home_template(project_folder: Union[Path, str]) -> None:
    """Create a home-page/landing-page template HTML file in the templates/ directory of the given rupantar project folder.

    Generate a basic HTML structure for a home page, including placeholders for the title, header,
    article content, blogposts list, and footer.
    The generated HTML file is saved to the 'templates' directory in the given rupantar project folder.

    Args:
        project_folder (str or Path): The path to the rupantar project folder where the 'templates' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        templates_path = Path(project_folder, "templates").resolve()
        home_template_path = Path(templates_path, "home_template.html.jinja").resolve()
        logger.info(f"{home_template_path.name} to be created at: {templates_path}")
        with open(home_template_path, "w") as temp_file:
            temp_data = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <title>{{ config.get('site-title') }}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content=" {{ config.get('desc') }}">
    <link rel="icon" href="{{ config.get('fav') }}" />
    <link rel="alternate" type="application/atom+xml" title="Recent blog posts" href="/rss.xml">
    <link rel="stylesheet" type="text/css" media="screen" href="{{ config.get('css') }}" />
</head>

<body>
    <header>
    <h1><a href="/">{% filter lower %} {{ title }} {% endfilter %}</a></h1>
    {{ header | safe }}
    </header>

    <section>
    <!-- article = markdown contents beyond the '---title=...etc.---' -->
    {{article | safe}}
    <ul>
    {% for post in posts %}
    {% if (post.showInHome is undefined) or post.showInHome %}
    <li>
    <time>
    {{ post.date.strftime('%Y-%m-%d') }}
    </time> : <a href="{{ post.url }}">{% filter lower %} {{ post.title }} {% endfilter %}</a>
    </li>
    {% endif %}
    {% endfor %}
    </ul>
    </section>

    <!--
    <section>
    {{ config.get('homefooter') }}
    </section>
    -->
    <footer>
    {{ footer | safe}}
    </footer>
</body>
</html>"""
            temp_file.write(temp_data)
            logger.info(
                f"{home_template_path.name} has been created at: {templates_path}"
            )
    except OSError as err:
        logger.exception(f"Error: Failed to create home_template.html.jinja\n{err}")


def create_note_template(project_folder: Union[Path, str]) -> None:
    """Create a generic blog-post template HTML file in the templates/ directory of the given rupantar project folder.

    Generate a basic HTML structure for a blog-post/note page, including placeholders for the title, header,
    article content, blogposts list, and footer.
    The generated HTML file is saved to the 'templates' directory in the given rupantar project folder.

    Args:
        project_folder (str or Path): The path to the rupantar project folder where the 'templates' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        templates_path = Path(project_folder, "templates").resolve()
        note_template_path = Path(templates_path, "note_template.html.jinja").resolve()
        logger.info(f"{note_template_path.name} to be created at: {templates_path}")
        with open(note_template_path, "w") as temp_file:
            temp_data = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="utf-8">
    <title>{{ post_title }}</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content=" {{ post_subtitle }}">
    <link rel="icon" href="{{ config.get('fav') }}" />
    <meta property="og:type" content="article" >
    <meta property="og:url" content="{{ url }}" >
    <meta property="article:modified_time" content="{{ date.strftime('%Y-%m-%d') }}" >

    <link rel="stylesheet" type="text/css" media="screen" href="{{ config.get('css') }}" />
    <link rel="alternate" type="application/atom+xml" title="Recent blog posts" href="/rss.xml">
    {% if metad %}  {{ metad }} {% endif %}
</head>

<body>
    <header>
    <h1>{{ post_title }} </h1>  
    </header>
    <article>
    {{ article | safe }}
    {% if date %} 
    <p># Last updated on <time>{{ date.strftime('%d %b %Y') }}.</time></p>
    {% endif %}
    </article>
    <footer>
    {{ footer | safe }}
    </footer>
</body>
</html>"""
            temp_file.write(temp_data)
            logger.info(
                f"{note_template_path.name} has been created at: {templates_path}"
            )
    except OSError as err:
        logger.exception(f"Error: Failed to create note_template.html.jinja\n{err}")


def create_feed_template(project_folder: Union[Path, str]) -> None:
    """Create a Really Simple Syndication feed template file in the templates/ directory of the given rupantar project folder.

    Note:
        Good RSS reference: https://www.w3schools.com/xml/xml_rss.asp
        RSS XML elements reference: https://www.w3schools.com/xml/xml_rss.asp#rssref

    Args:
        project_folder (str or Path): The path to the rupantar project folder where the 'templates' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        templates_path = Path(project_folder, "templates").resolve()
        feed_template_path = Path(templates_path, "feed_template.xml.jinja").resolve()
        logger.info(f"{feed_template_path.name} to be created at: {templates_path}")
        with open(feed_template_path, "w") as feed_file:
            feed_data = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">

<channel>

<title>{{ title }}</title>
<atom:link href="{{ url }}" rel="self" type="application/rss+xml" />
<link>{{ url }}</link>
<description>{{ subtitle }}</description>
<!-- Required channel child elements defined -->

<lastBuildDate>{{ last_date.strftime('%a, %d %b %Y %H:%M:%S') }}</lastBuildDate>
<language>en-ca</language>

<!-- Link to other blog posts -->
{% for post in posts %}{% if (post.showInHome is undefined) or post.showInHome %}
<item>
<title>{{ post.title }}</title>
<link>{{ config.get('url') }}{{ post.url }}</link>
<pubDate>{{ post.date.strftime('%a, %d %b %Y %H:%M:%S') }}</pubDate>
<guid isPermaLink="false">{{ config.get('url') }}{{ post.url }}</guid>
<description><![CDATA[{{ post.subtitle }} - {{ post.note }} ]]></description>
</item>
{% endif %}
{% endfor %}
</channel>

</rss>"""
            feed_file.write(feed_data)
            logger.info(f"Created {feed_template_path.name} at: {templates_path}")

    except OSError:
        logger.exception("Error: Failed to create feed_template.xml.jinja\n")


# content/ data
def create_header(project_folder: Union[Path, str]) -> None:
    """Create a header markdown file in the content/ directory of the given rupantar project folder.

    Generate a basic markdown structure for a header, including a navigation bar with a link to the homepage.
    The generated markdown file is saved to the 'content' directory in the given rupantar project folder.

    Args:
        project_folder (str or Path): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.
    """
    try:
        # TODO: Better md for this one!
        content_path = Path(project_folder, "content").resolve()
        header_content_path = Path(content_path, "header.md").resolve()
        logger.info(f"{header_content_path.name} to be created at: {content_path}")
        with open(header_content_path, "w") as header_file:
            header_data = """<nav>From content/header.md //
            <a href="/">homepage</a>
            </nav>"""
            header_file.write(header_data)
            logger.info(f"Created {header_content_path.name} at: {content_path}")
    except OSError:
        logger.exception("Error: Failed to create header.md\n")


def create_footer(project_folder: Union[Path, str]) -> None:
    """Create a footer markdown file in the content/ directory of the given rupantar project folder.

    Generate a basic markdown structure for a page's footer, including a mini-navigation 'bar' with links elsewhere.
    The generated markdown file is saved to the 'content' directory in the given rupantar project folder.

    Args:
        project_folder (str or Path): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        # TODO: Better md for this?
        content_path = Path(project_folder, "content").resolve()
        footer_content_path = Path(content_path, "footer.md").resolve()
        logger.info(f"{footer_content_path.name} to be created at: {content_path}")
        with open(footer_content_path, "w") as footer_file:
            footer_data = """<a href="/">homepage</a> //
<a href="https://github.com">git</a> //
<a href="https://linkedin.com">linkedin</a> 
*   powered by [Rupantar](/https://github.com/bhodrolok/rupantar)"""
            footer_file.write(footer_data)
            logger.info(f"Created {footer_content_path.name} at: {content_path}")
    except OSError:
        logger.exception("Error: Failed to create footer.md\n")


def create_home(project_folder: Union[Path, str]) -> None:
    """Create a home/landing page markdown file in the content/ directory of the given rupantar project folder.

    Generate a basic markdown structure for a simple home page, the body of the home page contents so to say.
    The generated markdown file is saved to the 'content' directory in the given rupantar project folder.

    Args:
        project_folder (str or Path): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        content_path = Path(project_folder, "content").resolve()
        home_content_path = Path(content_path, "home.md").resolve()
        logger.info(f"{home_content_path.name} to be created at: {content_path}")
        with open(home_content_path, "w") as homepage_file:
            homepage_data = """Welcome to Rupantar!
    <br> This is a sample homepage which can be edited at /content/home.md

    ** Rupantar links: **
    *   [Documentation](/).
    *   [Source code](/)."""
            homepage_file.write(homepage_data)
            logger.info(f"Created {home_content_path.name} at: {content_path}")
    except OSError:
        logger.exception("Error: Failed to create home.md\n")


def create_example_blog(project_folder: Union[Path, str]) -> None:
    """Create a sample blog markdown file in the content/ directory of the given rupantar project folder.

    Very barebones ngl.

    Args:
        project_folder (str or Path): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        content_path = Path(project_folder, "content").resolve()
        posts_content_path = Path(content_path, "notes").resolve()
        sample_blog_content_path = Path(posts_content_path, "example_blog.md").resolve()
        logger.info(
            f"{sample_blog_content_path.name} to be created at: {sample_blog_content_path}"
        )
        with open(sample_blog_content_path, "w") as post_file:
            post_data = (
                """---
title : "Sample Blog."
subtitle : "Sample subtitle"
date : {t}
---

# This is a sample note page which can be edited/renamed at /content/note/blog1.md
# This is heading 1, equivalent to <h1> </h1>!

## This is heading 2, equivalent to <h2> </h2>

### and so on....

**Bold text**

*italic text*

* unordered list item 1
* unordered list item 2

1. ordered list item 1
2. ordered list item 2

- [About Markdown](https://daringfireball.net/projects/markdown/)
- [Markdown syntax guide](/https://www.markdownguide.org/basic-syntax/)

Sample paragraph is written like this with lorem ipsum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."""
            ).format(t=datetime.now().strftime("%Y-%m-%d"))
            post_file.write(post_data)
            logger.info(
                f"Created {sample_blog_content_path.name} at:  {posts_content_path}"
            )
    except OSError:
        logger.exception("Error: Failed to create example_blog.md\n")


def create_static(project_folder: Union[Path, str]) -> None:
    """Create a static/ directory at the root of the given rupantar project folder along with a demo CSS for the static pages.

    The CSS is adopted from: https://nih.ar, the creator of pidgeotto, the OG project that rupantar is forked out of.

    Args:
        project_folder (str or Path): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        static_path = Path(project_folder, "static").resolve()
        demo_css_static_path = Path(static_path, "demo.css")
        logger.info(f"{demo_css_static_path.name} to be created at: {static_path}")
        with open(demo_css_static_path, "w") as css_file:
            css_data = """:root{--bg:#DDD;--txt:#333;--thm:#357670}
body{background:var(--bg);color:var(--txt);font:1.2em/1.6em sans-serif;max-width:900px;margin:7% auto auto;padding:0 5%}
h1,h2,h3{font-size:1em}
a{color:var(--thm);text-decoration:none}
a:hover{color:var(--bg);background-color:var(--thm);padding-top:3px}
header h1{color:var(--thm);font-size:1.2em;display:inline}
nav{font-weight:bold;display:inline}
ul{padding-left:20px;list-style-type:'-- ';line-height:1.4}
pre{border:1px solid var(--txt);padding:1em;overflow-x:auto}
code{background:var(--thm)}
pre code{background:none}
@media (prefers-color-scheme: dark){:root{--bg:#080C0C;--txt:#C6DFDD;--thm:#42938C}}
@media(max-width:480px){body{font:1em/1.4em sans-serif}}
            """
            css_file.write(css_data)
            logger.info(
                f"Created {demo_css_static_path.name} at: {demo_css_static_path}"
            )
    except OSError:
        logger.exception("Error: Failed to create demo.css\n")


def create_note(
    project_folder: Union[Path, str], post_filename: str, show_in_home=False
) -> None:
    """Create a new markdown note file in the notes directory of the given project folder.

    Note:
        Note = Blog = Post = BlogPost. Puns not fully intended.

    Generate the markdown file with a front-matter header containing page meta-data info like title, subtitle, showInHome flag, and date.
    The generated markdown file is saved to the 'notes' directory in the 'content' directory of the given project folder.

    Args:
        project_folder (str or Path): The path to the rupantar project folder, where the 'content' and 'notes' directories are also located.
        post_filename (str): The name of the markdown file to create.
        show_in_home (bool, optional): Flag to indicate whether the new note should be shown on the home page or not. Defaults to False.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        if not post_filename.lower().endswith(".md"):
            post_filename += ".md"

        content_path = Path(project_folder, "content").resolve()
        posts_path = Path(content_path, "notes").resolve()
        post_filename_path = Path(posts_path, post_filename).resolve()
        with open(post_filename_path, "w") as f:
            conf_data = (
                """---
title : "Title"
subtitle : "Subtitle"
showInHome : {s}
date : {t}
---
            """
            ).format(t=datetime.now().strftime("%Y-%m-%d"), s=show_in_home)
            f.write(conf_data)
            print(f"Created new page {post_filename}\nEdit it at: {post_filename_path}")
            logger.info(
                f"Created new page/post: {post_filename} at: {post_filename_path}"
            )

    except OSError:
        logger.exception("Error: Failed to create %s", post_filename)


@get_func_exec_time
def create_project(project_folder: str, user_choices: list[str]) -> None:
    """Initialize a rupantar project at the given project_folder path, with some optional user_choices list values.

    Creates the rupantar project skeleton and populates it with some default templates to be used when building the project.

    Note:
        If an exising rupantar project is found from the relative path at which the script is run, the folder will be overwritten from scratch.

    Args:
      project_folder (str): The name of the rupantar project.
      user_choices (list): A list with 3 string values to give user some freedom when creating the project and populating the config file.

    Raises:
        OSError: If any error opening or writing to the file/folder.

    """
    try:
        # Delete existing folder (https://stackoverflow.com/a/53492792)
        rupantar_project_path = Path(project_folder).resolve()
        if rupantar_project_path.exists():
            logger.warning(
                f"Existing rupantar project with name: {project_folder} found. Will overwrite it."
            )
            rmtree(rupantar_project_path)
            logger.warning(
                f"Old rupantar project: {project_folder} at {rupantar_project_path} removed. Recreating anew..."
            )
        while True:
            try:
                # mkdir(project_folder)
                Path.mkdir(Path(project_folder).resolve(), mode=511, parents=True)
                break
            except PermissionError:
                logger.exception(f"Error: Creating {project_folder}. Trying again...")
                continue
        logger.info(f"{project_folder} created at: {rupantar_project_path}")

        # Create directories for storing: Templates, static assets and page data (under contents)
        Path.mkdir(Path(rupantar_project_path, "templates").resolve())
        Path.mkdir(Path(rupantar_project_path, "content").resolve())
        Path.mkdir(Path(rupantar_project_path, "static").resolve())
        Path.mkdir(Path(rupantar_project_path, "content", "notes").resolve())

        # Generate default config, templates...
        create_config(rupantar_project_path, user_choices)
        # create_templates(project_folder)
        create_home_template(rupantar_project_path)
        create_note_template(rupantar_project_path)
        create_feed_template(rupantar_project_path)

        # ... and site contents
        create_static(rupantar_project_path)
        # # create_content(project_folder)
        create_header(rupantar_project_path)
        create_footer(rupantar_project_path)
        create_home(rupantar_project_path)
        create_example_blog(rupantar_project_path)

        # Finish init
        print(f"Project skeleton has been created at: {rupantar_project_path}")
        logger.info(
            f"Project skeleton has been initialized at: {rupantar_project_path}"
        )

    except OSError as err:
        logger.exception(f"Error: Failed to initialize rupantar project.\n{err}")
