# Reddit Automation Suite
A set of tools that allows the use of python plugins to easily process comment, submission, and modlog streams from PRAW (Python reddit API wrapper)

# Environment setup instructions
1. Ensure Python 3.6 or higher is installed
2. `cd` into project workspace
3. (Optional) to setup a local virtual environment you can run `python -m venv .venv`
    - On Windows in bash you can run: `.venv\Scripts\activate.bat`
    - On Mac OS and Linux you can run `source .venv/bin/activate`
4. run `pip install -r requirements.txt` to install dependencies

# Configuration
1. Rename config.example to config.yaml
    - Set `client` fields
    - Set `subreddit` name
    - Toggle which reddit streams you need access to under the `streams` field
        - Currently, the options are `comments`, `submissions`, `modlog`, and `modmail`.
    - Configure which plugins you want activated under the `plugins` field
2. All plugins must be placed into the plugins directory located at `/reddit_automation_suite/plugins/`
    - When toggling which plugins to run in config.yaml, the program finds the plugin by knowing which directory to look in, the filename of the main class, and the name of the main class to instantiate. 
    - Example plugin directory structure:
        ```bash
        plugins
        ├── vote_bot
        │   ├── main.py
        |   |   └──class Foo
        │   └── config.yaml
        └── events
            ├── baz.py
            |   └──class Bar
            ├── log.txt
            └── config.yaml
        ```
        The main config.yaml `plugins` section would look like this:
        ```yaml
        plugins:
        - "vote_bot.main.Foo"
        - "events.baz.Bar"
        ```
3. All loaded plugin classes are expected to have class methods of `consume_comment`, `consume_submission`, `consume_mod_log`, and `consume_modmail`. A `PluginBase` class can be found in `utils.py` and inherited from which has the aforementioned methods set as well as some other useful methods for loading config files. 

4. Support for storing data in a local sqlite db is a WIP, you can see current examples being used in `plugins/indie_sunday/indie_sunday.py`

# Usage
1. `cd` into project workspace
2. run `python -m reddit_automation_suite`

# Testing
1. `cd` into project workspace
2. run `python -m pytest tests/ --cov=lower`

# Architecture
![Image](https://i.imgur.com/Y4hXXxX.png)