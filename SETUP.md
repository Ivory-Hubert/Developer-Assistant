# Setup instructions

## Installing from PyPI (Easiest and recommended):
**Using uv:**
`uv tool install developer-assistant`

**Using pip:**
`pip install developer-assistant`

**Then use `da-ui` anywhere in your terminal to run it**

> **Tip: Once setup is complete and you start the program, an intro with all the necessary information will be displayed for you in the terminal.**


## Installing from a cloned repository:
**Using uv (recommended for clones):**
1. Open the program's root folder in your terminal.
2. Run `uv tool install .`
3. Then use `da-ui` anywhere in the system to run it.

**Using pip:**

**Option A - system-wide**
1. Open the program's root folder in your terminal.
2. Run `pip install .`
3. Then use `da-ui` anywhere in the system to run it.

**Option B - using a virtual environment**

*In this case I bet you know what you're doing.*


## No install, run from the repository:
**Use this command while root is open in the terminal:**
1. `uv sync`

This creates a local environment and installs all required dependencies.

**Now you can run the program from the root folder like this:**

2. `uv run -m DA.Interface`

You can then also create an `Interface.py` shortcut to use the program. (*Icons included.*)

(*Note that in this case the program will also run from the repo folder, not system-wide.*)

### Creating a shortcut on Linux:
1. **Make the exe script:**
```bash
nano ~/.local/bin/da-ui
```

2. **Write this, with your own repository location:**
```bash
#!/bin/bash
cd /home/.../.../Developer-Assistant && uv run -m DA.Interface
```

3. **Make the .desktop file:**
```bash
nano ~/.local/share/applications/da-ui.desktop
```

4. **Add the details:**
```bash
[Desktop Entry]
Type=Application
Name=Dev-Assistant
Comment=Markdown changelogs simplified
Exec=/home/.../.local/bin/da-ui
Icon=/home/.../.../Developer-Assistant/DA-icon.png
Terminal=true
Categories=Development;
```
