# Developer Assistant
[![PyPI version](https://img.shields.io/pypi/v/developer-assistant?logo=pypi&logoColor=white&color=blue)](https://pypi.org/project/developer-assistant/)

> **A lightweight TUI designed to simplify formatting of Markdown changelogs.**

* **Setup:** Start with [SETUP](./SETUP.md) to get started.

* **Changes:** Yes, I keep a [CHANGELOG](./CHANGELOG.md)

---

**Requirements:** Python 3.10 or later.

**Cross-platform:** Windows, Linux, macOS(*unverified*)


## Appearance

### Coloured, easy-to-use menus
![Changelog Menu](documents/images/changelog-menu.png)

### Beautiful changelog previews
Preview your Markdown changelogs directly in the terminal with Rich rendering:

![Changelog Preview](documents/images/md-preview.png)


## Introduction

### What does this tool do?
Developer Assistant is a lightweight TUI tool for automating and managing your changelogs. You can customize the templates to match your existing format, and use DA as a central hub to access every changelog and project folder you maintain.

You can manage as many projects as you like. Each project gets its own `.ini` file, created automatically through the menu based on the information you provide. These act as links that tell DA where your changelogs are and what's the last version number.

Your files are kept safe at all times. Before adding new changes, your existing `CHANGELOG.md` is automatically backed up. While editing, all changes are written to a temporary file first and only applied to the real changelog once you confirm them.


### Using the program.
1. **What *not* to do**

Don't change the folder structure or modify variable names inside `.ini` files.

2. **Features and information**

**The user's data (`Templates/`, `Projects/`, `memory.ini`) is stored in standard locations:**

Windows: `C:\Users\...\AppData\Roaming\da-ui\`

Linux: `~/.config/da-ui/`

macOS: `~/Library/Application Support/da-ui/`

The `da-ui/` folder will be created automatically.

You can access its content quickly when going to: `Main menu / Settings`

- *Customizable templates*

In the **local** `Templates/` folder you can modify the template contents to your liking - **just avoid changing the `{{placeholder}}` names**.

- *Linked projects all in one place*

The `Projects/` folder holds the `.ini` files you create when starting a new project with DA. 

- *Safe changelog updates*

Before applying any changes, your previous `CHANGELOG.md` is automatically backed up into your project folder. 
New changes are first written to a temporary file and only applied to the real changelog after you confirm them.
This ensures your existing changelog is never overwritten or corrupted, and you always have a fallback copy.
If the temporary changelog is present on startup you are prompted to remove or keep it.

- *Ease of navigation*

You can access files/folders and configuration straight from the menus, so you shouldn't find yourself searching through the program's directory or even your local user data very often.

- *Configuration*

The `memory.ini` file does exactly what you'd expect, it features:

> Last project

> Pinned projects

> Custom colour

Last project gets updated automatically, the rest are up to you.

- *`Ctrl+C` works everywhere to quickly exit DA.*


### Setting up your first project
For a dummy changelog to experiment with, navigate to `Main menu / Projects`, choose `Test-Project`, then choose option `4.` to start adjusting this projects paths. 

The `Test-Project/` folder is included in the programs root folder for repo clones and is safe to experiment with. If you installed from PyPI just make a `CHANGELOG.md` anywhere and point the `.ini` file to it.

Once configured, you can create as many changelog entries as you want by picking that project in the menu.


## Updating DA
Two possibilities, depending on how you installed.

### 1. Installed from PyPI
A. **Using uv:** `uv tool upgrade developer-assistant`

B. **Using pip:** `python -m pip install -U developer-assistant`


### 2. Installed from a local clone
*Run all terminal commands in the repo folder*

A. **Using uv:**
1. `git pull`
2. `uv tool install .`

B. **Using pip:**
1. `git pull`
2. `pip install .`

C. **No install, running from repo root:**

Just `git pull`
