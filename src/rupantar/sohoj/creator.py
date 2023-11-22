from os import chdir, mkdir, path, getcwd
from shutil import rmtree
from datetime import datetime
import logging

# Use root logger = same instance from start.py [ https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial ]
# 'Child loggers propagate messages up to the handlers associated with their ancestor loggers.'
logger = logging.getLogger()


def create_config(project_folder, user_choices):
    # Default name is config.yml + located in root of project folder
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
        config_file_path = path.join(path.abspath(project_folder), "config.yml")
        logger.info(f"config.yml file will be created at: {config_file_path}")
        with open(config_file_path, "w") as conf_file:
            conf_data = f"""# Required
title : Demo website    # Title in home page
url : {url}    # Site URL 

# Jinja templates
note_template : templates/note_template.html    # Template of note page
home_template : templates/home_template.html    # Template of home page
feed_template : templates/feed_template.xml     # Template of feed/RSS page
{custom_needed}custom_templates: 

# Directories
home_path : public      # Generated static files, served from here
content_path : content  # Markdown files (define page contents and front-matter metadata)
resource_path : static  # Static assets (css, js, image, etc.) 

home_md : content/home.md       # Home page stuff
header_md : content/header.md   # Header 
footer_md : content/footer.md   # Footer 

# Optional (Add custom configs here)
site-title : Demo Site Title!                     
css : demo.css 
desc : {desc}
mail : some@mail.com
                """
            conf_file.write(conf_data)
            logger.warning("Created config.yml at %s", config_file_path)
    except OSError:
        logger.exception("Error: Failed to create config.yml\n")


# templates
def create_home_template(project_folder):
    try:
        templates_path = path.join(project_folder, "templates")
        with open(path.join(templates_path, "home_template.html"), "w") as temp_file:
            temp_data = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <title>{{ config.get('site-title') }}</title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content=" {{ config.get('desc') }}">
    <!--<link rel="shortcut icon" href="{{ config.get('fav') }}" />-->
    <link rel="alternate" type="application/atom+xml" title="Recent blog posts" href="/rss.xml">
    <link rel="stylesheet" type="text/css" media="screen" href="{{ config.get('css') }}" />
</head>

<body>
    <header>
    <h1><a href="/">{% filter lower %} {{ title }} {% endfilter %}</a></h1>
    {{ header }}
    </header>

    <section>
    <!-- article = markdown contents beyond the '---title=...etc.---' -->
    {{article}}
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
    {{ footer }}
    </footer>
</body>
</html>
            """
            temp_file.write(temp_data)
            logger.info("Created home_template.html at %s", templates_path)
    except OSError:
        logger.exception("Error: Failed to create home_template.html\n")


def create_note_template(project_folder):
    try:
        templates_path = path.join(project_folder, "templates")
        with open(path.join(templates_path, "note_template.html"), "w") as temp_file:
            temp_data = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="utf-8">
    <title>{{ post_title }}</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content=" {{ post_subtitle }}">
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
    {{ article }}
    {% if date %} 
    <p># Last updated on <time>{{ date.strftime('%d %b %Y') }}.</time></p>
    {% endif %}
    </article>
    <footer>
    {{ footer }}
    </footer>
</body>
</html>
                """
            temp_file.write(temp_data)
            logger.info("Created note_template.html at %s", templates_path)
    except OSError:
        logger.exception("Error: Failed to create note_template.html\n")


def create_feed_template(project_folder):
    try:
        templates_path = path.join(project_folder, "templates")
        with open(path.join(templates_path, "feed_template.xml"), "w") as feed_file:
            feed_data = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">

<channel>
<title>{{title}}</title>
<atom:link href="{{ url }}" rel="self" type="application/rss+xml" />
<link>{{ url }}</link>
<description>{{ subtitle }}</description>
<lastBuildDate>{{ last_date.strftime('%a, %d %b %Y %H:%M:%S GMT') }}</lastBuildDate>
<language>en-IN</language>

<image>
<url>{{ config.get('url') }}/{{ config.get('pht') }}</url>
<title>{{ title }}</title>
<link>{{ url }}</link>
<width>32</width>
<height>32</height>
</image>

{% for post in posts %}{% if (post.showInHome is undefined) or post.showInHome %}
<item>
<title>{{ post.title }}</title>
<link>{{ config.get('url') }}{{ post.url }}</link>
<pubDate>{{ post.date.strftime('%a, %d %b %Y %H:%M:%S GMT') }}</pubDate>
<guid isPermaLink="false">{{ config.get('url') }}{{ post.url }}</guid>
            <description><![CDATA[{{ post.subtitle }} - {{ post.note }} ]]></description>
</item>
{% endif %}{% endfor %}
</channel>"""
            feed_file.write(feed_data)
            logger.info("Created feed_templat.xml at %s", templates_path)

    except OSError:
        logger.exception("Error: Failed to create feed_template.xml\n")


# content/ data
def create_header(project_folder):
    try:
        content_path = path.join(project_folder, "content")
        with open(path.join(content_path, "header.md"), "w") as header_file:
            header_data = """<nav> From content/header.md //
<a href="/">homepage</a
</nav>
            """
            header_file.write(header_data)
            logger.info("Created header.md at %s", content_path)
    except OSError:
        logger.exception("Error: Failed to create header.md\n")


def create_footer(project_folder):
    try:
        content_path = path.join(project_folder, "content")
        with open(path.join(content_path, "footer.md"), "w") as footer_file:
            footer_data = """<a href="/">homepage</a> //
<a href="https://github.com">git</a> //
<a href="https://linkedin.com">linkedin</a> 
*   powered by [Rupantar](/https://github.com/bhodrolok/rupantar)
            """
            footer_file.write(footer_data)
            logger.info("Created footer.md at %s", content_path)
    except OSError:
        logger.exception("Error: Failed to create footer.md\n")


def create_home(project_folder):
    try:
        content_path = path.join(project_folder, "content")
        with open(path.join(content_path, "home.md"), "w") as homepage_file:
            homepage_data = """Welcome to Rupantar!
    <br> This is a sample homepage which can be edited at /content/home.md

    ** Rupantar links: **
    *   [Documentation](/).
    *   [Source code](/).
            """
            homepage_file.write(homepage_data)
            logger.info("Created home.md at %s", content_path)
    except OSError:
        logger.exception("Error: Failed to create home.md\n")


def create_example_blog(project_folder):
    try:
        content_path = path.join(project_folder, "content")
        posts_path = path.join(content_path, "notes")
        with open(path.join(posts_path, "example_blog.md"), "w") as post_file:
            post_data = (
                """---
title : "Sample Blog."
subtitle : "Sample subtitle"
date : {t}
---

# This is a sample note page which can be edited/renamed at /content/note/blog1.md
# This is heading 1

## This is heading 2

### and so on....

**Bold**

*italic*

* list item 1
* list item 2

1. ordered list
2. ordered list

[About Markdown](https://daringfireball.net/projects/markdown/)
[Markdown syntax guide](/https://www.markdownguide.org/basic-syntax/)

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |


Sample paragraph is written like this with lorem ipsum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            """
            ).format(t=datetime.now().strftime("%Y-%m-%d"))
            post_file.write(post_data)
            logger.info("Created example_blog.md at %s", posts_path)
    except OSError:
        logger.exception("Error: Failed to create example_blog.md\n")


# static asset(s)
def create_static(project_folder):
    try:
        static_path = path.join(project_folder, "static")
        with open(path.join(static_path, "demo.css"), "w") as css_file:
            # adapted from nih.ar
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
            logger.info("Created demo.css at %s", static_path)
    except OSError:
        logger.exception("Error: Failed to create demo.css\n")


def create_note(project_folder, post_filename, show_home_page=True):
    try:
        if not post_filename.lower().endswith(".md"):
            post_filename += ".md"

        content_path = path.join(project_folder, "content")
        posts_path = path.join(content_path, "notes")
        with open(path.join(posts_path, post_filename), "w") as f:
            conf_data = (
                """---
title : "Title"
subtitle : "Subtitle"
showInHome : {s}
date : {t}
---
            """
            ).format(t=datetime.now().strftime("%Y-%m-%d"), s=show_home_page)
            f.write(conf_data)
            logger.info(post_filename + " is created at content/note/" + post_filename)

    except OSError:
        logger.exception("Error: Failed to create %s", post_filename)


def create_project(project_folder, user_choices):
    try:
        # Delete existing folder (https://stackoverflow.com/a/53492792)
        if path.exists(project_folder):
            logger.warning(f"Existing rupantar project with name: {project_folder} found. Overwriting...")
            rmtree(project_folder)
            logger.warning(f"Old {project_folder} removed. Proceeding to start anew...")
        while True:
            try:
                mkdir(project_folder)
                break
            except PermissionError:
                logger.exception(f"Error: Creating {project_folder}. Trying again...")
                continue
        # mkdir(project_folder)
        logger.info(f"{project_folder} created at: {path.abspath(project_folder)}")
        # Change cwd to new project folder
        chdir(project_folder)
        curr_dir = getcwd()
        logger.info(f"cwd is now: {curr_dir}")
        # Create directories for storing: Templates, static assets and page data (under contents)
        mkdir("templates")
        mkdir("content")
        mkdir("static")
        mkdir(path.join("content", "notes"))
        # Generate default config, templates and site contents
        project_folder = curr_dir
        logger.info(f"project_folder = {project_folder}")
        create_config(project_folder, user_choices)
        #create_templates(project_folder)
        create_home_template(project_folder)
        create_note_template(project_folder)
        create_feed_template(project_folder)

        create_static(project_folder)
        # # create_content(project_folder)
        create_header(project_folder)
        create_footer(project_folder)
        create_home(project_folder)
        create_example_blog(project_folder)
        # Finish init
        print(f"Project skeleton created at: {path.abspath(project_folder)}")
        logger.info(f"Project skeleton has been initialized at: {path.abspath(project_folder)}")

    except OSError:
        logger.exception("Error: Failed to initialize rupantar project\n")