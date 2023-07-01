from shutil import copytree, rmtree
from os import path, makedirs, chdir
from glob import glob
import yaml
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown

class Config:

    def __init__(self, config_file_path):

        # basic constructor for the class for instantiation
        # '_' variable = not intendeded to be used = throwaway value holder (in this case the filename without ext)
        _, extension = path.splitext(config_file_path)
        if extension == '.yaml' or extension == '.yml':
            with open(config_file_path, 'r') as yaml_file:
                config = yaml.safe_load(yaml_file)
        # TODO: Add TOML support
        else:
            raise ValueError(f"Config file format: {extension} is not supported!")

        # Dynamically set attributes to the instance for each key-value pair in the config file
        for key, val in config.items():
            setattr(self, key, val)

def build_project(project_folder, config_file_name):
    # Create Page
    def create_page(page_template, post_detail, md, filename):

        just_filename = path.basename(filename)
        post_template = Environment(loader=FileSystemLoader(searchpath = project_folder )).get_template(page_template)
        post_title = config.title
        post_date = post_data = posts_list = last_date = nextpage = post_meta = post_subtitle = ""
        post_path =  config.home_path

        if just_filename == "index.html":
            post_file = filename
            posts_list = posts
        elif just_filename.endswith(".html"):
            post_file = filename
            posts_list = posts
        elif just_filename.endswith(".xml"):
            post_file = filename
            posts_list = posts
            last_date = posts_list[0].get('date')
        elif post_detail is None :
            print(f"Converting: {just_filename} to .html format")
            post_file = filename.replace('.md','.html')

        else:
             # Read meta data from content/notes/*.md files
            post_title = post_detail.get("title")
            post_subtitle = post_detail.get("subtitle")
            post_date = post_detail.get("date")
            post_meta = post_detail.get("meta")
            #post_data = filename.split('/')
            post_path = path.join(project_folder, config.home_path)
            #print(f"post_path: {post_path}")
            #post_file = post_data[2].replace('.md','.html')
            # Convert to HTML
            post_file = path.basename(filename).replace('.md', '.html')
            print(f"OG filename: {path.basename(filename)}\t\t NEW filename: {post_file}")
            #post_data = post_data[1]
            post_data = path.dirname(filename)
            print(f'post_data: {post_data}')
            #print(f"post_data: {post_data}")

            makedirs(post_path,exist_ok=True)

        # Define where new .html/.xml file will be located
        # Eg: public/file.html || public/file.xml
        post_file_new = path.join(post_path, post_file)
        print(f"Creating: {post_file_new}")
        with open(post_file_new, 'w') as output_file:
            output_file.write(
                post_template.render(
                    title = config.title,
                    post_title=post_title,
                    post_subtitle=post_subtitle,
                    date=post_date,
                    metad=post_meta,
                    url=path.join(config.url, post_file),
                    article=markdown(md),
                    posts=posts_list,
                    home=config.home_md,
                    header=markdown(md_to_str(path.join(project_folder, config.header_md))),
                    footer=markdown(md_to_str(path.join(project_folder, config.footer_md))),
                    nextpage=nextpage,
                    last_date=last_date,
                    config = config.__dict__
                )
            )
        return post_file
    
    # Markdown file to string
    def md_to_str(md):
        with open(md,'r') as data:
            return data.read()


    # Program entry
    try:
        # Location of current file
        script_dir = path.dirname(path.dirname(path.abspath(__file__)))
        # Location of project folder with all contents 
        project_folder = path.join(script_dir, project_folder)
        # Location of config file, assumed to be in abovementioned project folder
        config_file = 'config.yml' if (config_file_name is None) else config_file_name
        config_file_path = path.join(config_file)
        # Change cwd to the pidgey project folder
        chdir((project_folder))
        # New Config object with data loaded from the config file
        config = Config(config_file_path)
        # Recreated home path with resource (static assets)
        resource_path_abs = path.join(project_folder, config.resource_path)
        # Home dir = Files to be served (eg: public/); web-accessible 
        home_path_abs = path.join(project_folder, config.home_path)
        # Clear out existing public/ folder
        if path.exists(home_path_abs):
            rmtree(home_path_abs)
        # Recreate home path with resource
        copytree(resource_path_abs, home_path_abs)
        
        #Create pages from content/notes/
        posts = []
        notes_path = path.join(config.content_path, 'notes')
        for each_note_md in glob( path.join(notes_path, "*.md") ):
            yaml_lines, ym, md = [],'',''
            with open(each_note_md) as infile:
                for s in infile:
                    if s.startswith('---'):
                        for s in infile:
                            if s.startswith('---'):
                                break;
                            else:
                                yaml_lines.append(s)
                        # ym = 'metadata' so stuff inside the --- ---
                        ym = ''.join(yaml_lines)
                        # md = rest of page contents outside the --- ---
                        md = ''.join(infile)
                        break;

            # Store file 'metadata', inside the front-matter, into post_detail
            post_detail=yaml.safe_load(ym)
            
            # Create blog pages
            if (post_detail is not None):
                post_url = create_page(config.note_template, post_detail, md, each_note_md)
                ymd = post_detail
                ymd.update({'url' : '/'+post_url})
                ymd.update({'note' : markdown(md)})
                posts += [ymd]
        
        #Sort posts based on date in descending order
        posts = sorted(posts, key=lambda post : post['date'], reverse=True)
        
        # Create other pages
        # home.
        create_page(config.home_template, None, md_to_str(config.home_md), "index.html")
        # RSS
        create_page(config.feed_template, None, md_to_str(config.home_md), "rss.xml")

    except:
        print("while building pidgey, some issue occured.")
        print("This can be due to \n\t1. Not a pidgey directory. \n\t2. Unknown file structure")
    
    else:
        print(f"Project built at: {path.join(project_folder, config.home_path)}.\tReady to serve...")


