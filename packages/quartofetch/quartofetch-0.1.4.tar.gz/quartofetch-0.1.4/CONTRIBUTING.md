# Contributing to Quarto Fetch

Thank you for considering contributing to Quarto Fetch! Here are some guidelines to help you get started:

## How to Contribute

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## Reporting Issues

If you find a bug or have a feature request, please create an issue on GitHub.

## Development Setup

1. Clone the repository.
2. Install the development dependencies:

   ```bash
   uv sync # or pip install ".[dev]"
   ```

3. Run tests:

   ```bash
    pytest
    ```

## Coding Standards and Tools

We use the following tools to maintain code quality and consistency:

- **uv** for environment and dependency management.
- **Ruff** for formatting and linting.
- **pytest** for testing.
- **Loguru** for logging.
