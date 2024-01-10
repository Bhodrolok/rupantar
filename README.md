<div align="center">
<h1>
    <img src="./assets/visuals/proj_logo.png" style="background-color:white" width="43px">
    <b> Rupantar </b>
    <p style="font-size: medium">No-frills website generation, powered by Python</p>
</h1>

<div align="center">

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7524d0f5c0b1459b9dc54d3fd42b146c)](https://app.codacy.com/gh/Bhodrolok/rupantar/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![CodeClimate Maintain. Badge](https://api.codeclimate.com/v1/badges/9e514a85a4f9a27a3895/maintainability)](https://codeclimate.com/github/Bhodrolok/rupantar/maintainability)

[![GitHub issues](https://img.shields.io/github/issues-raw/bhodrolok/rupantar?color=blue&style=plastic)](https://github.com/Bhodrolok/rupantar/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/bhodrolok/rupantar)](https://github.com/Bhodrolok/rupantar/issues?q=is%3Aissue+is%3Aclosed)
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

<details id="readme-top">
  <summary>Table of Contents 🚩</summary>
  <ol>
    <li><a href="#description">Description</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#dependencies">Dependencies</a></li>
    <li><a href="#install">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <ol>
      <li><a href="#qdemo">Quick Demonstration</a></li>
    </ol>
    <li><a href="#structure">Project Structure</a></li>
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

<h2 id="features"> Features :rocket: </h2>

1. Customizable using [Jinja2 templates](https://jinja.palletsprojects.com/en/3.0.x/templates/)
2. Fits well with multiple use cases
   - Blogging, personal knowledge base, portfolio, etc.
3. Completely [JavaScript-free](https://endtimes.dev/why-your-website-should-work-without-javascript/)
   - Trust the resilience of good ol' HTML and CSS
4. RSS and Atom [feed](https://indieweb.org/RSS) generation
5. Fast build times
6. Bundled web server with live reload on changes
7. Cross-platform
   - Runs in Windows, Linux, and macOS machines
8. Minimal system resource footprint

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="dependencies"> Dependencies :bridge_at_night: </h2>

Rupantar has the following dependencies:

- <a href="https://pypi.org/project/PyYAML/" target="_blank">PyYAML</a>:  Project configuration and page metadata management
- <a href="https://pypi.org/project/tomli/" target="_blank">tomli</a>:  Same as above for [TOML](https://toml.io/en/) enjoyers
    - **Not** required if running Python 3.11 or above

- <a href="https://pypi.org/project/Jinja2/" target="_blank">jinja2</a>:	Templating engine used to render the HTML/XML pages
- <a href="https://pypi.org/project/markdown2/" target="_blank">markdown2</a>:	Reading Markdown files
- <a href="https://pypi.org/project/xdg-base-dirs/" target="_blank">xdg-base-dirs</a>:  Getting location for app runtime data storage ('AppData')
   - as per the [XDG Base Dir spec](https://wiki.archlinux.org/title/XDG_Base_Directory)
   - mostly for storing logs when running rupantar


<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="install"> Installation :coconut: </h2>

- Rupantar needs [Python](https://www.python.org/downloads/) installed locally.
  - **CPython** version compatibility: Python interpreter **version 3.10 _or higher_**.

- [`pip`](https://pip.pypa.io/en/stable/installation/), Python's default package management tool, can be used.
- _If_ [`pipx`](https://pipx.pypa.io/stable/) is available, it is recommended to use that instead.

- Installation from **source**:
  - Install [Git](https://git-scm.com/downloads)
  - Clone this [git repository](https://github.com/bhodrolok/rupantar.git)
  - `cd` into the `rupantar` directory
  ```console
    $ pip install -r requirements
    ```

- Direct installation using **Git**:
  ```console
    $ pip install git+https://github.com/bhodrolok/rupantar
    ```

- Using **pipx**:
  ```console
    $ pipx install rupantar==0.9.5a0
    ```
<!-- NB: Any major differences b/w Windows and MacOS and GNULinux, mention here-->


<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="usage"> Usage :crab: </h2>

- NB: Rupantar is a pure CLI tool, without any GUI.

To get a comprehensive list of commands and options:
```console
$ rupantar -h
```

To get the detailed usage of a specific command:
```console
$ rupantar cmd_name -h
```

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="qdemo">Quick Demo :barber: </h2>

To initiate a project ( say for example `notun`):

```console
$ rupantar init notun
```
- NB: Some generic questions will be asked running this command in order to set up some configuration values.
- To avoid this, pass the `-s` or `--skip` flag after `init`.
  - They will be filled with some sane defaults.

To add a new post/page (say for example `kagoch`, to the existing `notun` project):

```console
$ rupantar new notun kagoch
```

To build the static pages (for `notun`):

```console
$ rupantar build notun
```

To preview the website locally:

```console
$ rupantar serve notun
```
- Useful for quick and simple testing via a local HTTP web server.

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="structure"> Project Structure :fork_and_knife: </h2>

The overall skeleton of a fully built & ready-to-serve rupantar project looks something like:
```
rupantar_project/
    ├── config.yml  <-- Config for the page title, CSS file, and other custom config (custom templates, etc.)
    ├── content/  <-- Directory to store Markdown files.
    │   ├── header.md
    │   ├── footer.md
    │   ├── home.md
    │   └── notes/  <-- Directory to store Markdown files for content of extra pages.
    │       └── example_blog.md
    └──static/  <-- Directory to store static content eg: CSS, images, etc.
    │   └── demo.css
    ├── public/   <-- Directory to store the generated static site.
    └── templates/  <-- Directory to store Jinja2 layouts for the pages.
        ├── home_template.html.jinja
        ├── note_template.html.jinja
        ├── your_custom_template.html.jinja
        └── feed_template.xml.jinja

```

Rupantar itself is developed with a "src layout" structure so as to follow a more modern, standardized, and organized way of managing everything. To read more about that, click <a href="#readme-top">here</a>.

A :construction: features roadmap of this Python project can be found [here](https://github.com/users/Bhodrolok/projects/3).

And lastly, there is also a [TODO.md](TODO.md) for some transparency and organization (and quick notes/documentation :P).

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="extra"> Development & Configuration :plate_with_cutlery:</h2>

- It is recommended to use [Poetry](https://github.com/python-poetry/poetry) for better dependency management, packaging, and release.
  - A big reason is the ease in managing virtual environments.
  - Why consider `venvs` in the first place? Well you get an isolated environment, better reproducibility, better dependency management, and (most importantly!) minimize risk of any conflicts with other existing Python projects/dependencies locally on the system. Especially if they were installed globally system-wide using `pip`.
  - Just overall makes the development process more smoother.

- After forking and cloning the repository:
  - Navigate to the cloned project directory.
  - Install **all** the dependencies, including the optional ones:
    ```console
    $ poetry install --with=dev,test,docu
    ```
  - Activate a virtual env:
    ```console
    $ poetry shell
    ```
  - Run rupantar:
    ```console
    $ poetry run rupantar -h
    ```


<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="contributing">Contributing :scroll: </h2>


This is an open source project. Suggestions, bug reports, feature requests, documentation improvements, etc. are more than welcome through [Pull Requests (PRs)](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) and [Issues](https://github.com/Bhodrolok/rupantar/issues).

The _usual_ steps for contributing via a PR are:

1. Fork this repository to your own GitHub account

2. Clone the repository to your machine

  ```console
$ git clone https://github.com/Bhodrolok/rupantar.git
  ```

3. `cd` to where you cloned the repo and create a local git branch

```console
$ git checkout -b new-feature-branch
```

4. Make your changes and commit them to that branch

```console
$ git commit -m "brief description about changes"
```

5. Push your changes to your remote fork

```conole
$ git push origin new-feature-branch
```

6. Create a new Pull Request!


<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>


<h2 id="license">License :bookmark:</h2>

This project is licensed under the [MIT License](./LICENSE).

_tldr_ is that `rupantar` is Free and Open Source Software (FOSS)!

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>

<h2 id="alternatives">Similar Projects :goat:</h2>

- [pidgeotto](https://github.com/niharokz/pidgeotto) - Primary inspiration for this project.
- [Pelican](https://github.com/getpelican/pelican) - Python-based
- [Jekyll](https://github.com/jekyll/jekyll) - Ruby-based
- [Hugo](https://github.com/gohugoio/hugo) - Go-based
- [Zola](https://github.com/getzola/zola) - Rust-based
- [Eleventy](https://github.com/11ty/eleventy) - JavaScript-based alternative to Jekyll
- Some more Python-based static site generators can be found [here](https://wiki.python.org/moin/StaticSiteGenerator).

<p align="right">(<a href="#readme-top">back to top :arrow_up: </a>)</p>

