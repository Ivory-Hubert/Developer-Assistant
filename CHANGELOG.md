# Changelog

All notable changes to Developer-Assistant(DA) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

DA assures the format stays consistent.

## [0.3.5] - 2026-03-19

### Added
- **Format & commit**

Turned `changelog_template.txt` into the changelog title, that the user can modify. Previously it was used for creating new changelogs, but this feature was quite useless. Since you could make new changelogs with the existsing "Add changes" option very well. So now formatting means this template is used to prepend the title to the changelog and the commit part means a custom `command` variable from the projects `.ini` file is used to run a command in the project folder (git for example).

### Changed
- **File size limits**

I realised the previous limit was way too big. Now, there are two limits. Under 10MB chagelogs will be rendered in the terminal with Rich. Under 20MB logs will be displayed as basic text and anything over that will be rejected.

- **UI tweaks**

When creating new changelogs the prompts use > instaed of : now. The same applies for adding changelog entries aswell. Reduced sleep command durations across the program. Turned the DA header dynamic with simple standard library logic to move away from having a fixed UI appearance.

### Fixed
- **Unified Markdown rendering**

Previously the `.md` preview for saving changelog entries and just viewing your existsing changelogs from the menu, were seperate instances in the code. This is inneficient and very lazy, so I modified the code to support two seperate entry points to `view_md()`. Also had to do some modifications to that function to support the new two-step size checks.


## [0.3.0] - 2026-03-16

### Added
- **Custom profiles**

With a new directory structure for user data to support endless profiles. 
To support and leverage the new system I added `owner` and `edited` variables to project `.ini` files. `memory.ini` takes care of tracking the active profile. The user can switch profiles and manage profile specific projects straight from the menus. The creation of a new profile requires just a one string input in `Main menu / Profiles`. The active profile is displayed on the top-left corner.

- **Extended atomic file operations**

Changelogs now use the same robust tempfile/replace system `.ini` files use.

- **File size checks**

DA wont try to open or display changelogs bigger than 100MB, since that's not very good on the terminal or your system... as I discovered.

- **Did I edit this project today?**

Now you know, since after every changelog creation/update the Project menu will show you if it was today, yesterday or whenever.

### Changed
- **Recover changelog backup**

Due to changelog updates being safer now, I transformed the changelog backup that was previously a `.md` file into `.bak`, with a simple option to restore it in project settings.

- **Optimized startup**

The loading bar that was purely decorative for a long time is now tied to runtime setup and initialization tasks, hence making it faster too.

### Fixed
- **Unclear separation of concerns**

`ConfigManager()` does not print messages anymore, instead returns them to `Interface()`. Also migrated the Projects menu from `Interface()` to `ProjectsManager()`, was truly a faux pas on my part to keep it there for so long.


## [0.2.5] - 2026-03-13

### Fixed
- **Writing changelogs to faulty project paths**

Removed a grand feature I discovered, the program wrote new changelogs to non-existing paths.

- **Misconfigured entry point and recursion**

Interface() now uses a proper run() function, also intro() won't call menu() after it finishes.

### Changed
- **Performance and efficiency updates**

Before this update every class had its own copy of ConfigManager() for `memory.ini`, and that's a problem, so now `memory.ini` is shared between classes. Also removed useless self. prefixes from some variables that didn't need them.

### Added
- **New indications about the project you're editing**

In the `Add changes` menu you can now see what project you're editing, and once you head to save changes you can see the last version number as you're promted for the new one.


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
