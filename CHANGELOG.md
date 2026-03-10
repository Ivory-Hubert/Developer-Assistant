# Changelog

All notable changes to Developer-Assistant will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [0.2.0] - 2026-03-10

### Fixed
- **Opening of projects.**

Fixed `ConfigManager` trying to read project `.ini` files that are mistyped in `memory.ini` or don't exist in `Projects/`.

### Changed
- **Turned DA into a package**

Changed the folder structure and `pyproject.toml` to include `Templates/` and defaults if users install the packaged tool system-wide.

- **Updated the documentation**

The intro is now separate from README. SETUP now accurately describes how to install the tool with uv, pip or make a shortcut, or just run it from root.

### Added
- **Migration and default logic**

Now that user data lives in their local OS-specific config folders, I decided a first run protocol is needed. So now with every update the default templates are packaged with DA and if they dont exist in the users config folder, they get copied there. Now the absence of a local `memory.ini` signals to DA that it's a first run. In that case `Projects/` spawns in with `Test-Project.ini` pre loaded, and `memory.ini` comes with just Test-Project pinned.


## [0.1.0] - 2026-03-07

### Added
- **Changelog management**

Create and edit changelogs using templates.

- **Auto-backup system**

Before changes get written to your changelog, the system creates a backup into your project folder.

- **Rich-powered Markdown**

Displays your changelogs in the terminal, in Markdown format.

- **Project management with automatic version tracking**



- **Terminal-based welcome screen**

Displays the rendered `README.md` file with a welcome screen, using a flag in the `memory.ini` file.

- **`Ctrl+C` support for a smooth exit throughout the program.**



### Fixed
- **Added file existence checks**

To prevent crashes and unwanted behaviour.


## [0.1.0-alpha] - 2026-02-17

### Added
- **First functionality achieved.**

The program creates new project .ini files and makes new changelogs, like this one.
