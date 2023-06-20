from os import chdir, mkdir, path
from datetime import datetime


def create_config(project_folder):
    # Default name is config.yml + located in root of project folder
    config_file_path = path.join(project_folder, 'config.yml')
    with open(config_file_path,'w') as conf_file:
        conf_data = (
            """# Required 
title : Demo website
url : yourdomain.tld
note_template : template/note_template.html   # Template of note page
home_template : template/home_template.html   # Template of home page
feed_template : template/feed_template.xml   # Template of feed/rss page
home_path : public  # After built, static files will be generated here
content_path : content # All post notes markdown location
resource_path : static # All css, js, image location
home_md : content/home.md # Homepage content
header_md : content/header.md # Header content
footer_md : content/footer.md # Footer content

# Optional Configuration, Add your own configs here
site-title : Demo Pidgeotto
css : demo.css
desc : Write anything that human and machine can understand.
mail : some@mail.com
            """)
        conf_file.write(conf_data)
        print(f"Created config.yml at {config_file_path}")

# templates
def create_home_template(project_folder):
    templates_path = path.join(project_folder, 'templates')
    with open(path.join(templates_path,'home_template.html'),'w') as temp_file:
        temp_data = (
        """<!DOCTYPE html>
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
</html>""")
        temp_file.write(temp_data)
        print(f'Created home_template.html at: {templates_path}')
    
def create_note_template(project_folder):
    templates_path = path.join(project_folder, 'templates')
    with open(path.join(templates_path,'note_template.html'),'w') as temp_file:
            temp_data = (
            """<!DOCTYPE html>
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
</html>""")
            temp_file.write(temp_data)
            print(f'Created note_template.html at: {templates_path}')

def create_feed_template(project_folder):
    templates_path = path.join(project_folder, 'templates')
    with open(path.join(templates_path,'feed_template.xml'),'w') as feed_file:
        feed_data = (
            """<?xml version="1.0" encoding="UTF-8"?>
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
 </channel>""")
        feed_file.write(feed_data)
        print(f'Created feed_template.xml at: {templates_path}.')

# content/ data
def create_header(project_folder):
    content_path = path.join(project_folder, 'content')
    with open(path.join(content_path,'header.md'),'w') as header_file:
        header_data = (
            """<nav> From content/header.md //
<a href="/">homepage</a
</nav>
        """)
        header_file.write(header_data)
        print(f'Created header at: {content_path}.')
    
def create_footer(project_folder):
    content_path = path.join(project_folder, 'content')
    with open(path.join(content_path,'footer.md'),'w') as footer_file:
        footer_data = (
            """<a href="/">homepage</a> //
<a href="https://github.com">git</a> //
<a href="https://linkedin.com">linkedin</a> 
*   powered by [Rupantar](/https://github.com/bhodrolok/rupantar)
        """)
        footer_file.write(footer_data)
        print(f'Created footer at: {content_path}.')

def create_home(project_folder):
    content_path = path.join(project_folder, 'content')
    with open(path.join(content_path,'footer.md'),'w') as homepage_file:
        homepage_data = (
            """Welcome to Rupantar.
<br> This is a sample homepage which can be edited at /content/home.md

** Rupantar links: **
*   [Documentation](/).
*   [Source code](/).
        """)
        homepage_file.write(homepage_data)
        print(f'Created homepage at: {content_path}.')

def create_example_blog(project_folder):
    content_path = path.join(project_folder, 'content')
    posts_path = path.join(content_path, 'notes')
    with open(path.join(posts_path,'example_blog.md'),'w') as post_file:
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


Sample paragraph is written like this with lorem ipsum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """).format(t=datetime.now().strftime("%Y-%m-%d"))
        post_file.write(post_data)
        print(f'Example blog created at {posts_path}.')

def createNote(project_folder, post_filename, show_home_page = True):
    try:
        if not post_filename.lower().endswith('.md'):
            post_filename+='.md'
        with open(path.join(project_folder,'content','note',post_filename),'w') as f:
            conf_data = (
            """---
title : "Title"
subtitle : "Subtitle"
showInHome : {s}
date : {t}
---
            """).format(t=datetime.now().strftime("%Y-%m-%d"), s=show_home_page)
            f.write(conf_data)
            print(post_filename+" is created at content/note/"+post_filename )
    except:
        print("while generating page "+post_filename+", some issue occured.")
        print("This can be due to \n\t1. Not a pidgey directory. \n\t2. Invalid filename")

def create_project(project_folder):
    try:
        # Create project folder
        mkdir(project_folder)
        # Use location of current file to get to parent directory(oustide sohoj/)
        script_dir = path.dirname(path.dirname(path.abspath(__file__)))
        # Location of project folder with all contents (absolute)
        project_folder = path.join(script_dir, project_folder)
        # Change cwd to new project folder
        chdir((project_folder))
        # Create directories for storing: Templates, static assets and page data (under contents)
        mkdir('templates')
        mkdir('content')
        mkdir('static')
        mkdir(path.join('content','notes'))
        # Generate default config, templates and site contents
        create_config(project_folder)
        #create_templates(project_folder)
        create_home_template(project_folder)
        create_note_template(project_folder)
        create_feed_template(project_folder)
        #create_content(project_folder)
        create_header(project_folder)
        create_footer(project_folder)
        create_home(project_folder)
        create_example_blog(project_folder)

        print(f"Project skeleton created at: {project_folder}")
    except:
        print("while generating pidgey "+ project_folder + ", some issue occured.")
        print("This can be due to \n\t1. Pidgey already exists.\n\t2. Memory issue.\n\t3. Invalid input.\n\t4. If none of these, report to developer.")

