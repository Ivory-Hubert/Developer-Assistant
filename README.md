# Developer Assistant

> **New here?** Start with [SETUP.md](./SETUP.md) to get started!

**Requirements:** Python 3.13 or later.

**Cross-platform:** Windows, Linux, macOS(unverified)

**Dependencies:** Listed in `requirements.txt`

## Appearance

### Coloured, easy-to-use menus
![Changelog Menu](Documents/images/changelog-menu.png)

### Beautiful changelog previews
Preview your Markdown changelogs directly in the terminal with Rich rendering:

![Changelog Preview](Documents/images/md-preview.png)

## Introduction

### What does this tool do?
Developer Assistant is a lightweight TUI tool for automating and managing your changelogs. You can customize the templates to match your existing format, and use DA as a central hub to access every changelog and project folder you maintain.

You can manage as many projects as you like. Each project gets its own `.ini` file, created automatically through the menu based on the information you provide. These act as links that tell DA where your changelogs are and what's the last version number.

Your files are kept safe at all times. Before adding new changes, your existing `CHANGELOG.md` is automatically backed up. While editing, all changes are written to a temporary file first and only applied to the real changelog once you confirm them.

### Documentation.
Documentation includes `SYSTEM STRUCTURE.txt`, example -and default files. If you ever need to replace a file, the example/default files can also be used for that.

`SYSTEM STRUCTURE.txt` - explains what module does what and how the menu flows.

`CHANGELOG.md` - this programs own changelog.

### Using the program.
1. **What *not* to do**

Don't change the folder structure or modify variable names inside `.ini` files.

2. **Features and information**

If you want a dummy changelog to experiment with, open `Projects/Test-Project.ini` and adjust the file paths to match your system.

The included `Test-Project/` folder is part of the program and is easy to experiment with.

Once configured, you can create as many changelog entries as you want by picking that project in the menu.

- *Customizable templates*

Explore the `Templates/` folder and modify the template contents to your liking - **just avoid changing the `{{placeholder}}` names**.

- *Linked projects all in one place*

The `Projects/` folder holds the `.ini` files you create when starting a new project with the program. 
Temporary changelogs also appear there.

- *Safe changelog updates*

Before applying any changes, your previous `CHANGELOG.md` is automatically backed up into your project folder. 

New changes are first written to a temporary file and only applied to the real changelog after you confirm them.

This ensures your existing changelog is never overwritten or corrupted, and you always have a fallback copy.

- *Ease of navigation*

You can access *most* files/folders and configuration straight from the menus, so you shouldn't find yourself searching through the program's directory very often.

- *Configuration*

The `memory.ini` file does exactly what you'd expect, it features:

> Last project

> Pinned projects

> Custom colour

> Toggle intro

Last project gets updated automatically, the rest are up to you. `Toggle intro` is on by default.

- *`Ctrl+C` works everywhere to quickly exit DA.*

### "I deleted this file, what now?"
No problem:

`memory.ini` - copy `memory example.ini` to the main folder and rename it.

`Any changelog template` - `default changelog.md`, copy that to `Templates/` 

**and make** = {

changelog_template.txt,

entry_template.txt,

header_template.txt

}

**Of course cut its contents up to match the description of the file you lost.**

*Or download new files if you want.*
