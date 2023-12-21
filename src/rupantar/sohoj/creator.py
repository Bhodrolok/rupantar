from pathlib import Path
from shutil import rmtree
from datetime import datetime
from logging import getLogger
from rupantar.sohoj.utils import get_func_exec_time, resolve_path

# Use root logger = same instance from start.py [ https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial ]
# 'Child loggers propagate messages up to the handlers associated with their ancestor loggers.'
logger = getLogger()


def create_config(project_folder: str, user_choices: list[str | None]) -> None | OSError:
    """Create a configuration file for a rupantar project based on some user input.

    Expects the first param to be a project folder and the second to be a list of user choices.
    If the user skips providing any choices, default values will be used instead.
    Using these, a new 'config.yml' file is generated at the root of the rupantar project folder.
    The configuration file includes settings for the rupantar project (eg: site URL, templates, directories, and any other optional custom configurations).

    Args:
      project_folder (str): The relative path to the rupantar project folder where the configuration file will be created
      user_choices (list of str): A list of user choices to set some configuration values

    Raises:
      OSError: If any error opening or writing to file

    TODO: Maybe use TOML instead of YAML for default?
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
        "" if (user_choices[-1] and user_choices[-1].strip()) else default_conf_values[-1]
    )
    try:
        config_file_path = resolve_path(project_folder, "config.yml")
        logger.info(
            f"{config_file_path.name} file to be generated at: {config_file_path}"
        )
        with open(config_file_path, "w") as conf_file:
            conf_data = f"""# Required
title : Demo website    # 'Title'/'Name' in home/landing page (NOT <title> HTML element)
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
site_title : Demo Page Title
css : demo.css
desc : {desc}   # page description
mail : some@mail.com
"""
            conf_file.write(conf_data)
            logger.info(f"Created {config_file_path.name} at {config_file_path}")
            return None
    except OSError as err:
        logger.exception(f"Failed to create config.yml: {err}")


def create_home_template(project_folder: str) -> None | OSError:
    """Create a home-page/landing-page Jinja2 template file in the templates/ directory of the given rupantar project folder.

    Generate a basic HTML structure for a home page, including placeholders for the title, header,
    article content, blogposts list, and footer.
    The generated HTML file is saved to the 'templates' directory in the given rupantar project folder.

    Args:
        project_folder (str): The path to the rupantar project folder where the 'templates' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        templates_path = resolve_path(project_folder, "templates")
        home_template_path = resolve_path(templates_path, "home_template.html.jinja")
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


def create_note_template(project_folder: str) -> None | OSError:
    """Create a generic blog-post Jinja2 template file in the templates/ directory of the given rupantar project folder.

    Generate a basic HTML structure for a blog-post/note page, including placeholders for the title, header,
    article content, blogposts list, and footer.
    The generated HTML file is saved to the 'templates' directory in the given rupantar project folder.

    Args:
        project_folder (str or Path): The path to the rupantar project folder where the 'templates' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        templates_path = resolve_path(project_folder, "templates")
        note_template_path = resolve_path(templates_path, "note_template.html.jinja")
        logger.info(f"{note_template_path.name} to be created at: {templates_path}")
        # https://getoutofmyhead.dev/x-ua-compatible/
        with open(note_template_path, "w") as temp_file:
            temp_data = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="utf-8">
    <title>{{ page_title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content=" {{ page_desc }}">
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
    <h1>{{ page_title }} </h1>
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


def create_feed_template(project_folder: str) -> None | OSError:
    """Create a Really Simple Syndication feed template file in the templates/ directory of the given rupantar project folder.

    Note:
        Good RSS reference: https://www.w3schools.com/xml/xml_rss.asp
        RSS XML elements reference: https://www.w3schools.com/xml/xml_rss.asp#rssref

    Args:
        project_folder (str): The path to the rupantar project folder where the 'templates' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    """
    try:
        templates_path = resolve_path(project_folder, "templates")
        feed_template_path = resolve_path(templates_path, "feed_template.xml.jinja")
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
def create_header(project_folder: str) -> None | OSError:
    """Create a header markdown file in the content/ directory of the given rupantar project folder.

    Generate a basic markdown structure for a header, including a navigation bar with a link to the homepage.
    The generated markdown file is saved to the 'content' directory in the given rupantar project folder.

    Args:
        project_folder (str): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.
    TODO: Better content
    """
    try:
        content_path = resolve_path(project_folder, "content")
        header_content_path = resolve_path(content_path, "header.md")
        logger.info(f"{header_content_path.name} to be created at: {content_path}")
        with open(header_content_path, "w") as header_file:
            header_data = """<nav>From content/header.md //
            <a href="/">homepage</a>
            </nav>"""
            header_file.write(header_data)
            logger.info(f"Created {header_content_path.name} at: {content_path}")
    except OSError:
        logger.exception("Error: Failed to create header.md\n")


def create_footer(project_folder: str) -> None | OSError:
    """Create a footer markdown file in the content/ directory of the given rupantar project folder.

    Generate a basic markdown structure for a page's footer, including a mini-navigation 'bar' with links elsewhere.
    The generated markdown file is saved to the 'content' directory in the given rupantar project folder.

    Args:
        project_folder (str): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    TODO: Better content
    """
    try:
        content_path = resolve_path(project_folder, "content")
        footer_content_path = resolve_path(content_path, "footer.md")
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


def create_home(project_folder: str) -> None | OSError:
    """Create a home/landing page markdown file in the content/ directory of the given rupantar project folder.

    Generate a basic markdown structure for a simple home page, the body of the home page contents so to say.
    The generated markdown file is saved to the 'content' directory in the given rupantar project folder.

    Args:
        project_folder (str): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.
    TODO: Better content
    """
    try:
        content_path = resolve_path(project_folder, "content")
        home_content_path = resolve_path(content_path, "home.md")
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


def create_example_blog(project_folder: str) -> None | OSError:
    """Create a sample blog markdown file in the content/ directory of the given rupantar project folder.

    Very barebones ngl.

    Args:
        project_folder (str): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.
    TODO: Better content, stickied TOC on left/right side, anchors on headings, etc.
    """
    try:
        content_path = resolve_path(project_folder, "content")
        posts_content_path = resolve_path(content_path, "notes")
        sample_blog_content_path = resolve_path(posts_content_path, "example_blog.md")
        logger.info(
            f"{sample_blog_content_path.name} to be created at: {sample_blog_content_path}"
        )
        with open(sample_blog_content_path, "w") as post_file:
            post_data = (
                """---
title : "Sample Blog."
desc : "Sample description about this page or blogpost."
date : {t}
---

This is a sample note (or 'post') page which can be edited at /content/notes/example_blog.md. You can also add other pages here!

# This is a heading, equivalent to the \<h1> element in regular HTML

Sample paragraphs are like this. New paragraphs are created by leaving a blank line between them.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vel velit iaculis, pretium nulla quis, pharetra eros. Suspendisse rhoncus aliquam elit, vel dapibus quam condimentum ac. Mauris mollis sollicitudin tristique. Nunc dolor neque, lobortis et urna et, congue ultrices felis. Donec egestas, nulla bibendum gravida dapibus, ex nunc imperdiet magna, vitae consectetur nibh neque et dolor. Duis vulputate ipsum ipsum, in interdum quam euismod et. Nam pulvinar volutpat egestas. Mauris urna ligula, consectetur nec odio vitae, tempor scelerisque urna. Quisque sagittis, eros non porta efficitur, massa ante dignissim leo, finibus scelerisque turpis libero at risus. Pellentesque eu mauris sem. Duis commodo lectus a augue pellentesque, placerat fringilla ex consectetur.

## Text styling & emphasis

**Bold text sample**, *italic text sample*

~~Strikethroughs supported as well!~~

### Linking

Wrap your text in [links](https://www.markdownguide.org/basic-syntax/) using the \[ ] brackets, followed by the URL in \( ) parentheses.

- ProTip: You can ignore or **escape** characters by using the '\' character to prevent them being formatted

# Lists

* unordered list - item 1
* unordered list - item 2

---

Line breaks like the one above using \---

1. ordered list - item 1
2. ordered list - item 2
    1. indented ordered list item
        a. more indentation is ***possible***

+ [About Markdown](https://daringfireball.net/projects/markdown)
+ [Markdown syntax guide](/https://www.markdownguide.org/basic-syntax)

Sample paragraphs are written like this.

> Blockquotes like this with the '>'
> - You can do this too!
> > Reckon they can even be nested!
> > > Think I should stop here **tho**


Aenean enim dolor, tincidunt eget ante nec, dictum auctor tellus. Sed dictum velit quis nibh dictum vulputate. Etiam luctus justo elit, fermentum consectetur tellus sagittis sed. Praesent nibh lacus, dapibus at diam at, faucibus tempus augue. Donec et nulla velit. Pellentesque id congue justo, ac suscipit ex. Donec pretium nec odio id sodales. Vivamus ullamcorper posuere tortor, in porta mi rutrum sit amet. Sed sit amet semper nunc, volutpat laoreet augue. Cras malesuada imperdiet dui, sit amet euismod tortor. Phasellus convallis velit vitae ligula porta, ac pretium lorem pretium. Nulla facilisi. Donec rhoncus enim turpis, vel hendrerit lectus mattis feugiat."""
            ).format(t=datetime.now().strftime("%Y-%m-%d"))
            post_file.write(post_data)
            logger.info(
                f"Created {sample_blog_content_path.name} at:  {posts_content_path}"
            )
    except OSError:
        logger.exception("Error: Failed to create example_blog.md\n")


def create_static(project_folder: str) -> None | OSError:
    """Create a static/ directory at the root of the given rupantar project folder along with a demo CSS for the static pages.

    The CSS is adopted from: https://nih.ar, the creator of pidgeotto, the OG project that rupantar is forked out of.

    Args:
        project_folder (str): The path to the rupantar project folder where the 'content' directory is located.

    Raises:
        OSError: If any error opening or writing to the file.

    TODO: Update CSS & overall design?
    """
    try:
        static_path = resolve_path(project_folder, "static")
        demo_css_static_path = resolve_path(static_path, "demo.css")
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
            logger.info(f"Created {demo_css_static_path.name} at: {demo_css_static_path}")
    except OSError:
        logger.exception("Error: Failed to create demo.css\n")


def create_note(
    project_folder: Path | str, post_filename: str, show_in_home=False
) -> None | OSError:
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
def create_project(project_folder: str, user_choices: list[str | None]) -> None | OSError:
    """Initialize a rupantar project at the given project_folder path, with some optional user_choices list values.

    Creates the rupantar project skeleton and populates it with some default Jinja2 templates to be used when building the project & rendering content.

    Note:
        If an exising rupantar project is found from the relative path at which the script is run, the folder will be overwritten from scratch.

    Args:
      project_folder (str): The name of the rupantar project.
      user_choices (list): A list with 3 string values to give user some freedom when creating the rupantar project and populating the config file.
      Currently, they are all optional and as such can be None.

    Raises:
        OSError: If any error opening or writing to the file/folder.
        PermissionError

    """
    try:
        rupantar_project_path = resolve_path(project_folder)
        # Delete existing folder (https://stackoverflow.com/a/53492792)
        # TODO: Notify user?
        if rupantar_project_path.exists():
            logger.warning(
                f"Existing rupantar project with name: {project_folder} found. Will overwrite it."
            )
            rmtree(rupantar_project_path)
            logger.warning(
                f"Old rupantar project: {project_folder} at {rupantar_project_path} removed. Recreating anew..."
            )
        # TODO: Maybe try a few times before giving up?
        while True:
            try:
                # rwxrwxrx after umask 002
                Path.mkdir(rupantar_project_path, mode=511, parents=True)
                break
            except PermissionError:
                logger.exception(f"Error: Creating {project_folder}. Trying again...")
                continue
        logger.info(f"{project_folder} created at: {rupantar_project_path}")

        # Create directories for storing: Templates, static assets and page data (under content)
        Path.mkdir(resolve_path(rupantar_project_path, "templates"))
        Path.mkdir(resolve_path(rupantar_project_path, "content"))
        Path.mkdir(resolve_path(rupantar_project_path, "static"))
        Path.mkdir(resolve_path(rupantar_project_path, "content", "notes"))

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

        # Finish init-ing
        print(f"rupantar project skeleton created at: {rupantar_project_path}")
        logger.info(f"Project skeleton has been initialized at: {rupantar_project_path}")

    except OSError as err:
        logger.exception(f"Error: Failed to initialize rupantar project.\n{err}")
