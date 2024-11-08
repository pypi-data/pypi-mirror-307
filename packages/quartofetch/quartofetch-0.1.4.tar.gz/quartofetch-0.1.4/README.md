# Quarto Fetch

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool for managing multiple Quarto paper repositories in a research project. It automatically fetches, updates, and organizes Quarto paper repositories while maintaining their build caches.

## Features

- 📦 Manage multiple Quarto paper repositories in a single project
- 🔄 Automatically fetch and update papers from Git repositories
- 🏗️ Support for both manuscript and default Quarto project types
- ❄️ Smart handling of Quarto freeze directories
- 📋 Detailed logging with progress tracking
- ⚡ Efficient updates by tracking commit hashes
- 🛡️ Built-in validation and error handling

## Installation

We recommend using `uv` for installation. First, install `uv` if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Quick Run (Recommended)

Use `uvx` to run `quartofetch` directly without installation:

```bash
uvx quartofetch
```

### Permanent Installation

If you prefer to install the tool permanently:

```bash
uv tool install quartofetch
```

### Development Installation

For development work:

```bash
git clone https://github.com/MitchellAcoustics/quartofetch
cd quartofetch
uv sync
```

## Quick Start

1. Create a configuration file `research/_paper_sources.yml`:

```yaml
papers:
  - repo_url: "https://github.com/username/paper1"
    target_folder: "paper1"
    branch: "main"  # optional

  - repo_url: "https://github.com/username/paper2"
    target_folder: "paper2"
    commit: "abc123"  # optional, pin to specific commit
```

1. Run the fetcher:

```bash
# Using uvx (recommended)
uvx quartofetch

# Or with specific options
uvx quartofetch --config path/to/config.yml --force --log-level DEBUG

# If permanently installed
quartofetch --config path/to/config.yml
```

## Project Structure

The tool expects and creates the following directory structure:

```bash
your-research-project/
├── research/
│   ├── _paper_sources.yml
│   └── papers/
│       ├── paper1/
│       │   ├── _quarto.yml
│       │   ├── paper.qmd
│       │   └── ...
│       └── paper2/
│           ├── _quarto.yml
│           ├── manuscript.qmd
│           └── ...
└── _freeze/
    └── research/
        └── papers/
            ├── paper1/
            │   └── ...
            └── paper2/
                └── ...
```

## Configuration

### Paper Sources (`_paper_sources.yml`)

| Field           | Description          | Required |
| --------------- | -------------------- | -------- |
| `repo_url`      | Git repository URL   | Yes      |
| `target_folder` | Local folder name    | Yes      |
| `branch`        | Git branch to use    | No       |
| `commit`        | Specific commit hash | No       |

### Command Line Options

| Option        | Description                | Default                       |
| ------------- | -------------------------- | ----------------------------- |
| `--config`    | Path to configuration file | `research/_paper_sources.yml` |
| `--force`     | Force update all papers    | `False`                       |
| `--log-level` | Set logging level          | `SUCCESS`                     |
| `--debug`     | Enable debug logging       | `False`                       |
| `--log-file`  | Path to log file           | None                          |

## Error Handling

The tool includes comprehensive error handling for:

- Git operation failures
- Network timeouts
- Authentication issues
- Invalid configurations
- File system operations

## Development

### Requirements

- Python 3.12+
- Git

### Testing

```bash
# Install development dependencies
uv sync # or pip install ".[dev]"

# Run tests
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
