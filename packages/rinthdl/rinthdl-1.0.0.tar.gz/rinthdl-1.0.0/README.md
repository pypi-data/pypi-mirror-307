# Rinth DL

Rinth DL is a command-line tool for searching, downloading, and managing Minecraft mods,
modpacks, resource packs, shaders, datapacks, and plugins from [Modrinth](https://modrinth.com/).
It simplifies the process of automating mod downloads and their dependencies
and allows you to manage modpacks using a JSON configuration file.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Searching for Projects](#searching-for-projects)
  - [Downloading a Project](#downloading-a-project)
  - [Managing Modpacks](#managing-modpacks)
- [Examples](#examples)
- [Notes](#notes)
- [Error Handling](#error-handling)
- [License](#license)

## Features

- **Search** for Minecraft projects (mods, resource packs, etc.) on Modrinth.
- **Download** your favourite mod, shader, etc. (even a specific version)
- Automatically find **dependencies** when downloading whole modpacks.
- Manage and download your **modpacks** via a simple JSON configuration file.
- Supports various **project types**: mods, resource packs, shaders, plugins, etc.
- Compatible with all **platforms/loaders**: Fabric, Forge, Minecraft, Iris, etc.

## Installation

Install the package using pip or pipx
```bash
pipx install rinthdl
```

## Usage

### Searching for Projects

Use the `rinth-search` command to search for projects on Modrinth.

**Example:**

```bash
rinth-search sodium
```

This command will display a list of projects matching the search query,
including titles, slugs, IDs, URLs, and descriptions.

### Downloading a Project

Use the `rinth-util` command to perform various operations related to a project.

#### Available Operations:

- `get_id`: Fetch the project ID using the project slug.
- `get_versions`: Fetch all versions of a project.
- `get_version`: Fetch a specific version of a project.
- `get_dependencies`: Fetch dependencies of a project version.
- `get_project_meta`: Fetch metadata of a project.
- `download`: Download a project.

#### Command Syntax:

```bash
rinth-util <operation> <slug> [--game_version <game_version>] [--platform <platform>] [--project_version <project_version>] [--path <download_path>]
```

#### Parameters:

- `<operation>`: The operation to perform (see above).
- `<slug>`: The project slug (e.g., `sodium`).
- `--game_version`: The Minecraft game version (e.g., `1.20`).
- `--platform`: The platform/loader (e.g., `fabric`, `forge`, `minecraft`, `iris`).
- `--project_version`: The specific project version (e.g., `1.5.0`). Leave empty to get the latest version.
- `--path`: The path to download the file to (required when using the `download` operation).

#### Examples:

- **Get the project ID of Sodium:**

  ```bash
  rinth-util get_id sodium
  ```

- **Get all versions of Sodium for Minecraft 1.20 on Fabric:**

  ```bash
  rinth-util get_versions sodium --game_version 1.20 --platform fabric
  ```

- **Download the latest version of Sodium for Minecraft 1.20 on Fabric:**

  ```bash
  rinth-util download sodium --game_version 1.20.1 --platform fabric --path .
  ```

- **Download a specific version of Sodium:**

  ```bash
  rinth-util download sodium --game_version 1.20 --platform fabric --project_version mc1.20-0.4.10 --path /path/to/download
  ```
  
### Managing Modpacks

Use the `rinth-pack` command to manage modpacks via a JSON configuration file.

#### Modpack Configuration File

Create a JSON file (e.g., `modpack.json`) with the following structure:

```json
{
  "name": "Modpack 1",
  "game_version": "1.20",
  "path": "/path/to/download",
  "deps": "True",
  "projects": [
    {
      "name": "sodium",
      "version": "",
      "platform": "fabric",
      "type": "mod"
    },
    {
      "name": "fabric-api",
      "version": "",
      "platform": "fabric",
      "type": "mod"
    },
    {
      "name": "dramatic-skys",
      "version": "1.5.3.27vs",
      "platform": "minecraft",
      "type": "resourcepack"
    },
    {
      "name": "complementary-reimagined",
      "version": "",
      "platform": "iris",
      "type": "shader"
    }
  ]
}
```

#### Fields:

- **`name`**: Name of the modpack.
- **`game_version`**: Minecraft game version (e.g., `1.20`).
- **`path`**: The base path to download the mods to.
- **`deps`**: Whether to download dependencies (`"True"` or `"False"`).
- **`projects`**: A list of project definitions.

Each project definition includes:

- **`name`**: The slug of the project on Modrinth (e.g., `sodium`).
- **`version`**: The specific version to download (leave empty string for the latest version).
- **`platform`**: The platform/loader (e.g., `fabric`, `forge`, `minecraft`, `iris`).
- **`type`**: The type of project (`mod`, `resourcepack`, `shader`, etc.).

#### Running the Modpack Script

```bash
rinth-pack <modpack_file>
```

**Example:**

```bash
rinth-pack modpack.json
```

This command will download all specified projects to the paths determined
by the `path` and `type` fields in your configuration.

## Examples

### Example 1: Search for a Mod

```bash
rinth-search sodium
```

### Example 2: Download a Mod with Dependencies

Create a `modpack.json` file:

```json
{
  "name": "Awesome Modpack",
  "game_version": "1.20",
  "path": "~/modpacks/awesome",
  "deps": "True",
  "projects": [
    {
      "name": "sodium",
      "version": "",
      "platform": "fabric",
      "type": "mod"
    },
    {
      "name": "fabric-api",
      "version": "",
      "platform": "fabric",
      "type": "mod"
    },
    {
      "name": "dramatic-skys",
      "version": "1.5.3.27vs",
      "platform": "minecraft",
      "type": "resourcepack"
    },
    {
      "name": "complementary-reimagined",
      "version": "",
      "platform": "iris",
      "type": "shader"
    }
  ]
}

```

Run the modpack script:

```bash
rinth-pack modpack.json
```

**Output:**

```
Downloading assets for Awesome Modpack
Should I create path /home/your-name/modpacks/awesome? (y|N): y
✔️ Successfully downloaded sodium.
✔️ Successfully downloaded fabric-api.
✔️ Successfully downloaded dramatic-skys.
ℹ️ Dramatic-skys has a possible dependency for https://modrinth.com/project/fabricskyboxes
ℹ️ Template for your modpack.json: {"name": "fabricskyboxes", "version": "", "platform": "fabric", "type": "mod"}
✔️ Successfully downloaded complementary-reimagined.
```

## Notes

- The `rinth-pack` command automatically creates subdirectories under the specified `path` based on the `type` of
each project (e.g., `mods`, `resourcepacks`, `shaderpacks`).
- If `deps` is set to `"True"`, dependencies will be searched for each project.
If a dependency is not already listed in the `projects` list, it will inform you and provide a json template to add it.


## Error Handling

- The program has error handling to manage network issues, missing projects, invalid inputs, etc.
- Error messages start with `❌` and provide details about the issue.
- Common errors include:
  - Project not found.
  - No versions found matching the specified criteria.
  - Network connectivity problems.


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 License.
See the [LICENSE](LICENSE) file for details.
