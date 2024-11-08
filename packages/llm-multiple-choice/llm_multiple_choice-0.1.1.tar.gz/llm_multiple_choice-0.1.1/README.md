# LLM Multiple Choice

A Python library for having an LLM fill out a multiple-choice questionnaire about the current state of a chat.

## Features

- Composible with any LLM provider -- this library generates LLM prompts and validates responses,
  but leaves the actual LLM calls to you.
- Flexible questionnaire structure.
- Simple API for using the questionnaire results in code.

## Installation

You can install the library using pip:

```bash
pip install llm-multiple-choice
```

If you're using Poetry:

```bash
poetry add llm-multiple-choice
```

## Usage

This library helps you create multiple-choice questionnaires for LLMs to fill out.

### Creating a Questionnaire

```python
from llm_multiple_choice import ChoiceManager, DisplayFormat

# Create a questionnaire
manager = ChoiceManager()

# Add a section with choices
section = manager.add_section("Assess the sentiment of the message.")
positive_sentiment = section.add_choice("The message expresses positive sentiment.")
neutral_sentiment = section.add_choice("The message is neutral in sentiment.")
negative_sentiment = section.add_choice("The message expresses negative sentiment.")

# Get the prompt to send to your LLM
prompt = manager.prompt_for_choices(DisplayFormat.MARKDOWN)
```

### Processing LLM Responses

The library enforces these rules for LLM responses:
- Must contain only numbers corresponding to valid choices
- Numbers must be separated by commas
- Each number can only appear once
- Cannot be empty

Process the response:
```python
try:
    choices = manager.validate_choices_response(llm_response)
    # Check which choices were selected
    if choices.has(positive_sentiment):
        print("Choice 1 was selected")
except InvalidChoicesResponseError as e:
    print(f"Invalid response: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Setting Up for Development

To set up the project for development:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/deansher/llm-multiple-choice.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd llm-multiple-choice
   ```

3. **Install dependencies using Poetry**:

   ```bash
   poetry install
   ```

   This will install all the required packages in a virtual environment.

You can either activate the virtual environment in a shell by running `poetry shell`
or run commands directly using `poetry run <command>`.

### Editing in VSCode

To ensure VSCode uses the correct Python interpreter from the Poetry environment:

1. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac).
2. Select `Python: Select Interpreter`.
3. Choose the interpreter that corresponds to the project's virtual environment. It should be listed with the path to `.venv`.

If the virtual environment is not listed, you may need to refresh the interpreters or specify the path manually.

### Running Tests

`poetry run pytest`

### Adding Dependencies

To add a new dependency to the project:

- For regular dependencies:

  ```bash
  poetry add <package_name>
  ```

- For development dependencies (e.g., testing tools):

  ```bash
  poetry add --group dev <package_name>
  ```

This updates the `pyproject.toml` and `poetry.lock` files accordingly.

## Release Process

This project uses GitHub Actions for automated testing and publishing to PyPI.

### Making a Release

1. Update version in `pyproject.toml`
2. Create a new Release on GitHub:
   - Go to the repository's Releases page
   - Click "Create a new release"
   - Choose "Create a new tag" and enter the version (e.g., `v0.1.0`)
   - Add release notes describing the changes
   - Click "Publish release"
3. GitHub Actions will automatically:
   - Run all tests and type checking
   - Build the package
   - Publish to PyPI if all checks pass

### Manual Publishing

If needed, you can publish manually using the build script:

```bash
# Publish to TestPyPI
./scripts/build_and_publish.sh

# Publish to production PyPI
./scripts/build_and_publish.sh --production
```

### Local Development Integration

When developing applications that use this library, you may want to test changes to the library without publishing them to PyPI. You can achieve this using either Poetry or pip's editable install feature.

#### Using Poetry

Poetry's path dependency feature makes local development straightforward:

1. Clone this repository alongside your project:
   ```bash
   git clone https://github.com/deansher/llm-multiple-choice-py.git
   ```

2. In your project's `pyproject.toml`, replace the PyPI dependency with a path dependency:
   ```toml
   [tool.poetry.dependencies]
   llm-multiple-choice = { path = "../llm-multiple-choice-py", develop = true }
   ```

   Or use the Poetry CLI:
   ```bash
   poetry remove llm-multiple-choice
   poetry add --editable ../llm-multiple-choice-py
   ```

The `develop = true` flag creates a symlink to the library's source, allowing you to modify the library code and immediately see the effects in your project without reinstalling.

#### Using pip

If you're using pip, you can use its editable install feature:

1. Clone this repository alongside your project:
   ```bash
   git clone https://github.com/deansher/llm-multiple-choice-py.git
   ```

2. Install the package in editable mode:
   ```bash
   pip install -e ../llm-multiple-choice-py
   ```

The `-e` flag tells pip to install the package in "editable" mode, creating a link to the source code instead of copying it. This allows you to modify the library code and see changes immediately without reinstalling.


## License

This project is licensed under the MIT License - see the LICENSE file for details.
