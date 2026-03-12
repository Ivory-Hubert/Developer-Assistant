# Developer Assistant

## Installing from PyPI
**Using uv:**
`uv tool install developer-assistant`

**Using pip:**
`pip install developer-assistant`

**Then use `da-ui` anywhere in your terminal to run it**

> **Tip:** Once setup is complete and you start the program, an intro with all the necessary information will be displayed for you in the terminal.

## Updating DA
Two possibilities, depending on how you installed.

A. **Using uv:** `uv tool upgrade developer-assistant`

B. **Using pip:** `python -m pip install -U developer-assistant`

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

Now make an optional `Test-Project/` folder with a `CHANGELOG.md` in it anywhere on your system and point the `.ini` file to it.

Once configured, you can create as many changelog entries as you want by picking that project in the menu.
