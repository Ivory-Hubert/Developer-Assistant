# Developer-Assistant

## Introduction

### Setting up your first project
For a dummy changelog to experiment with, navigate to `Main menu / Projects`, choose `Test-Project`, then choose option `4.` to start adjusting this projects paths. 

The `Test-Project/` folder is included in the programs root folder for repo clones and is safe to experiment with. If you installed from an URL just make a `CHANGELOG.md` anywhere and point the `.ini` file to it.

Once configured, you can create as many changelog entries as you want by picking that project in the menu.

> *This quick guide is also at the end of the README for future reference*

### Using the program.
1. **What *not* to do**

Don't change the folder structure or modify variable names inside `.ini` files.

2. **Features and information**

**Your user data (`Templates/`, `Projects/`, `memory.ini`) is stored in standard locations:**

Windows: `C:\Users\...\AppData\Roaming\da-ui\`

Linux: `~/.config/da-ui/`

macOS: `~/Library/Application Support/da-ui/`

**The `da-ui/` folder has been created automatically. Updates won't overwrite it, only you can default it.
You can access its content quickly when going to: `Main menu / Settings`**

- *Customizable templates*

Explore the `Templates/` folder and modify the template contents to your liking - **just avoid changing the `{{placeholder}}` names**.

- *Linked projects all in one place*

The `Projects/` folder holds the `.ini` files you create when starting a new project with the program. 

- *Safe changelog updates*

Before applying any changes, your previous `CHANGELOG.md` is automatically backed up into your project folder. 
New changes are first written to a temporary file and only applied to the real changelog after you confirm them.
This ensures your existing changelog is never overwritten or corrupted, and you always have a fallback copy.

- *Ease of navigation*

You can access files/folders and configuration straight from the menus, so you shouldn't find yourself searching through the program's directory or even your local user data very often.

- *Configuration*

The `memory.ini` file does exactly what you'd expect, it features:

> Last project

> Pinned projects

> Custom colour

Last project gets updated automatically, the rest are up to you.

- *`Ctrl+C` works everywhere to quickly exit DA.*
