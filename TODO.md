# Rupantar task tracker

A :construction: features roadmap of this Python project can be found [here](https://github.com/users/Bhodrolok/projects/3).

### Left-TODO

get it?!

- [ ] Better docs for contributing to & developing the project `rupantar` including poetry scripts, dev workflow, tasks, tests etc.

- [ ] Application screenshots/gifs showing usage in the `README`

- [ ] Change variable names in config
	- [ ] `home_path` :luc_arrow_big_right: `output_dir`
	- [ ] RE-CHECK IF NEEDED: Overall prepare for new flag/option like `-o/--output-dir`
		- This is prob not needed given it can be edited in the `config` file

- [ ] Mention bit about stable + development version ( `main` vs `develop`) branches
	* Why this workflow instead of just a single `main`?
		* More systematic approach to managing changes +  Better separation between development and stable/release ready

### :hammer: W.I.P. :wrench:

- [ ] Also add these flags on top:
	- [ ] CI/CD (passing/failed)
	- [ ] Coverage (x%)
	- [x] License (MIT)
	- [ ] Python versions supported (if published to PyPi) like (python 3.7, 3.8.. 3.11)
		- [ ] Need to publish to Python Package Index (PyPI)
	- [x] Code Quality via Codacy (grade A?)
	- [x] Code Maintainability via Code Climate

### :dart: Completed ✓

- [x] Add this `TODO.md` file
- [x] Uncomment `watchfiles` dependency in `pyproject.toml`
  - Prob a `main`-dependency for the project...

- [x] Add a 'Similar Projects' section in the README with links to: [ zola, metalsmith, etc.]

- [x] Add list of features of `rupantar` in README

- [x] Also add `MIT License` picture in `License` section in `README.md`, like just above the text...

- [x] CLI --> `init`: more interactive, series of prompts (for config.yml creation) ==> more intuitive?!

- [x] Mention OS + Python(CPython) version compatibility: `needs Python interpreter (version 3.7?? or higher) to run`

- [x] Mention installation method: `pipenv/pdm/etc`, instead of standard source installation via `pip` i.e. *global Python interpreter* (installing packages globally), why use venv or something like that?
	- [x] Isolated environment, better reproducibility and dependency management, prevent conflicts of existing Python projects/dependencies on system, overall more secure? xDDD
	- [x] Direct installation? (aka **Building/Installation from source**)
		* Install Python version 3.8 (confirm!) or newer
		* Install Git version (??) or newer
		* Clone git repo, cd, (pip install if not already) `python3 start.py -h`
	- [x] Another way of regular install, this time directly via `git`:
		* `pip install git+https://github.com/bhodrolok/rupantar`
		* Might need to setup properly for this to work...

- [x] Logging:
	- [x] By default, `rupantar` writes logs to the following locations:
		- Linux (*Nix? xD*): ~/.config/rupantar/logs
		- macOS: path
		- Windows: %USERPROFILE%\AppData\Roaming\rupantar\logs
		- Accomplished using XDG-base-dirs library, local app config data directory will have the logs.
	- Need to find way to implement this (DONE-Nov 22-23 2023)

- [x] Resolve src-layout based import problems with `Poetry`
	- [x] https://stackoverflow.com/a/76317566

- [x] Make server also build when called?
	- [x] Optional, default behavior:
		1. Serve = Build + Serve
		2. Serve = Serve only
			1. (`-b/--build` flag to do 1.) 🤷
			2. Currently done as default i.e. `serve()` calls `build_project()`

