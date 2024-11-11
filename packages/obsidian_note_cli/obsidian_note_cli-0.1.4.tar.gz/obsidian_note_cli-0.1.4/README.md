# Obsidian Note CLI

`obsidian_note_cli` is a command-line tool for creating well-structured notes in Obsidian, complete with front matter metadata like creation date, tags, and status. This tool is designed for users who frequently take notes and want to streamline their note-taking workflow using Obsidian and the command line.

It goes well along with [Daniel Miessler's Fabric](https://github.com/danielmiessler/fabric), as it processes content passed through the stdin as default.


## Features

- Create notes with customizable front matter fields: `created_at`, `tags`, `status`, `source`, and more.
- Specify note content via a file or piped input (Linux-style `stdout | stdin`).
- Set default values for `created_at` at today's date.
- Configuration via environment variables for `vault` and `path`, with sensible defaults

## Installation

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for managing dependencies and packaging (optional but recommended)
- [pipx](https://pipxproject.github.io/pipx/) for globally installing CLI tools

### Step-by-Step Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/guglielmo/obsidian_note_cli.git
   cd obsidian_note_cli
   ```

2. **Build the Package with Poetry**

   ```bash
   poetry build
   ```

### Step 3: Install with pipx

Ensure that `pipx` is installed on your system. Then, use `pipx` to install the latest version of the CLI tool globally:

```bash
pipx install dist/obsidian_note_cli-<VERSION>-py3-none-any.whl
```
   
Replace <VERSION> with the latest version of your package (e.g., 0.1.0).

To check the current version, refer to the version specified in the pyproject.toml file or check the release information in your repository if published.

This makes `obsidian-note` available as a command globally, isolated from other Python environments.


Alternatively, if you are frequently updating and testing new versions, you can specify a specific version or install directly from your local directory after building:

```bash
pipx install dist/obsidian_note_cli-$(poetry version -s)-py3-none-any.whl
```

This command dynamically uses the current version from pyproject.toml by extracting it with poetry version -s.


## Usage

### Basic Usage

To create a note, specify at least the title, vault, and tags:

```bash
obsidian-note --title "My First Note" --vault "MyVault" --path "Notes" --tags "tag1,tag2"
```

This command saves a note in the specified vault and path with the provided title and tags.

### Using Interactive Mode

To enter parameters interactively, use the `--interactively` flag:

```bash
obsidian-note --interactively
```

### Example with Piped Content

You can pipe content into `obsidian-note`:

```bash
echo "This is the note content" | obsidian-note --title "My Piped Note" --vault "MyVault" --path "Notes" --tags "piped,content"
```

### Options

- `--title`: Title of the note.
- `--vault`: Obsidian vault name (default can be set via environment variable `VAULT`).
- `--path`: Path within the vault to save the note (default can be set via environment variable `PATH`).
- `--tags`: Comma-separated list of tags.
- `--status`: Optional status for the note.
- `--created_at`: Date in `YYYY-MM-DD` format (defaults to today).
- `--interactively`: Flag to enter parameters interactively.
- `content`: The content of the note, provided via a file or stdin.

## Configuration via Environment Variables

You can set default values for `vault` and `path` using environment variables:

```bash
export OBSIDIAN_VAULT="MyVault"
export OBSIDIAN_PATH="Notes"
```

This configuration allows you to avoid specifying `--vault` and `--path` for each note.

## Examples

1. **Create a Basic Note**

   ```bash
   obsidian-note --title "Daily Log" --vault "WorkVault" --path "Logs" --tags "daily,log" --status "in-progress"
   ```

2. **Create a Note with Interactive Mode**

   ```bash
   obsidian-note --interactively
   ```

3. **Pipe Content into a Note**

   ```bash
   echo "This is piped content" | obsidian-note --title "Piped Note" --vault "MyVault" --path "Notes" --tags "example,pipe"
   ```

4. **Use with fabric**

   ```bash
   fabric -u https://zettelkasten.de/introduction/ | summarize | \
   obsidian-note --path="09.ReadingList" --source=https://zettelkasten.de/introduction/
   ```

   This is a bit awkward, as for the duplication of the URL, an idea would be to define a bash function:

   ```bash
   function process_note_summarize() {
    local url="$1"
    fabric -u "$url" | summarize | \
    obsidian-note --source="$url" "$@"
   }
   ```

   so that the whole process of reducing the content of the URL to markdown, summarizing it through the AI and sending it to Obsidian, at a specific folder of the default vault, could be expressed as:

   ```bash
   process_note_summarize "https://zettelkasten.de/introduction/" \
      --path 09.ReadingList --tags self_improvement formation 
   ```


## Development

If you want to modify the tool, follow these steps to set up a development environment:

1. Clone the repository and navigate into it:

   ```bash
   git clone https://github.com/yourusername/obsidian_note_cli.git
   cd obsidian_note_cli
   ```

2. Install dependencies using `poetry`:

   ```bash
   poetry install
   ```

3. Run the tool locally with `poetry`:

   ```bash
   poetry run obsidian-note --title "Test Note" --vault "TestVault" --path "TestPath" --tags "test"
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## Contact

For questions or suggestions, please contact [your.email@example.com](mailto:your.email@example.com).
