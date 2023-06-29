<div align="center">
<h1>
    <a name="readme-top"></a>
    <img src="./assets/visuals/proj_logo.png" style="background-color:white" width="42px">
    <b> Rupantar </b>
    <p style="font-size: medium">No-frills website generation, powered by Python</p>
</h1>

<div align="center">

[![GitHub issues](https://img.shields.io/github/issues-raw/bhodrolok/rupantar?color=blue&style=plastic)](https://github.com/Bhodrolok/rupantar/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/bhodrolok/rupantar)](https://github.com/Bhodrolok/rupantar/issues?q=is%3Aissue+is%3Aclosed)
[![Python Style Guide](https://img.shields.io/badge/style%20guide-Google-yellow.svg?style=flat&logo=python&logoColor=white)](https://google.github.io/styleguide/pyguide.html)
[![Pull Requests](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat&logo=cachet&logoColor=red)](https://github.com/Bhodrolok/rupantar/pulls)

<!--
<p>Documentation available<a href="https://github.com/Bhodrolok/JobAppTrackr/tree/docs" target="_blank"> here </a></p>
-->

</div>

<h3> <a href="http://ipa-reader.xyz/?text=%C9%BEu%CB%90p%C9%91n%CB%88t%C9%94%C9%BE&voice=Raveena"> /ɾuːpɑnˈtɔɾ/ </a> (Bengali)  </h3>
<h4> transformation</h4>


<!--
<h3> Built using </h3>

[![react](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)
[![.net](https://img.shields.io/badge/--blue?style=for-the-badge&logo=.net&logoColor=white)](https://protonmail.com)

-->
</div>

---

<details>
  <summary>Table of Contents 🚩</summary>
  <ol>
    <li><a href="#description">Description</a></li>
    <li><a href="#dependencies">Dependencies</a></li>
    <li><a href="#install">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#structure">Project Structure</a></li>
    <!--<li><a href="#features">Features</a></li> 
    <li><a href="#shots">Screenshots</a></li>-->
    <li><a href="#extra">Configuration</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

---

<h2 id="description"> Description :ear_of_rice: </h2>

Fork of <a href="https://github.com/niharokz/pidgeotto" target="_blank">pidgeotto</a>

Rupantar is a command-line tool that enables quick generation of simple, minimally themed, static websites with extensive support for customizations.  

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>

<h2 id="dependencies"> Dependencies :bridge_at_night: </h2>

Rupantar has the following dependencies:

- <a href="https://pypi.org/project/PyYAML/" target="_blank">PyYAML</a>:  Reading config and setting page metadata
- <a href="https://pypi.org/project/toml/" target="_blank">TOML</a>:  Reading data for page contents/metadata
- <a href="https://pypi.org/project/Jinja2/" target="_blank">jinja2</a>:	Templating engine used to render the HTML/XML pages
- <a href="https://pypi.org/project/markdown2/" target="_blank">markdown2</a>:	Reading Markdown files


<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="install"> Installation :coconut: </h2>

- Ensure [Python](https://www.python.org/downloads/) is installed locally.
  - **CPython** version compatibility: needs Python interpreter (**version 3.7 or higher**)

- Installation from source:
  - Install [Git](https://git-scm.com/downloads)
  - Clone this [git repository](https://github.com/bhodrolok/rupantar.git)
  - `cd` into `rupantar` directory
  - ```console
    $ pip install -r requirements
    ``` 

- Direct installation using **Git**:
  - ```console
    $ pip install git+https://github.com/bhodrolok/rupantar
    ```
<!-- NB: Any major differences b/w Windows and MacOS and GNULinux, mention here-->


<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="usage"> Usage :crab: </h2>

To get a comprehensive list of commands and flags:
```console
$ rupantar -h
```


To initiate a project called `notun`:

```console
$ rupantar init notun
```
- NB: You will be asked some generic questions when running this command in order to set up some configuration values. 
- To avoid this, pass the `-s` or `--skip` flag after `init`

To add a new post/page, lets call it `kagoch`, to `notun`:

```console
$ rupantar new notun kagoch
```

To build the static pages for `notun`:

```console
$ rupantar build notun
```

To preview the website, you can test it by serving via a local server:

```console
$ rupantar serve notun
```

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="structure"> Project Structure :fork_and_knife: </h2>

The overall skeleton of the project looks something like this
```
rupantar_project/
    ├── config.yml
    ├── content/
    │   ├── header.md
    │   ├── footer.md
    │   ├── home.md
    │   └── notes/
    │       └── example_blog.md
    └──static/
    │   └── demo.css
    ├── public/
    └── templates/
        ├── home_template.html
        ├── note_template.html
        └── feed_template.xml
```

* config.yml:	Configurations for the page title, name, CSS file, js file, and other custom configurations such as custom templates.
* static:	Directory to store static content eg: CSS, js, image data, etc.
* content:	Directory to store Markdown files. 
* template:	Directory to store Jinja2 layouts for the pages.
* public: Directory to store generated static files.

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="extra"> Configuration :plate_with_cutlery:</h2>

<p>TODO</p>

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="contributing">Contributing :scroll: </h2>

This is an open source project. Suggestions, bug fixes, documentation improvements, translations, etc. are welcome through Pull Requests and Issues.

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="license">License :bookmark:</h2>

This project is licensed under the [MIT License](./LICENSE).

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>

<h2 id="alternatives">Similar Projects :goat:</h2>

- [pidgeotto](https://github.com/niharokz/pidgeotto) - Primary inspiration for this project.
- [pelican](https://github.com/getpelican/pelican)
- [eleventy](https://github.com/11ty/eleventy)
- [zola](https://github.com/getzola/zola)

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>

