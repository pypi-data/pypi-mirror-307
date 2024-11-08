# Magic 8 Ball Python Package

![Build Status](https://github.com/software-students-fall2024/3-python-package-magic-eight/actions/workflows/python-app.yml/badge.svg)

A fun and lighthearted Python package that emulates the classic Magic 8 Ball toy. This package allows users to ask questions and get random, playful responses. Built with rigorous software engineering practices, it serves as a joyful addition to any developer's toolbox.

## Features

This package includes the following functions:
- `get_questions(language, count=0)`: Retrieve a list of sample questions.
- `ask_question(language, question="")`: Ask a question and receive a random response.
- `shake_ball(language, shake_time=10)`: Shake the ball to get another response, with optional delay.
- `get_answers(language, count=0)`: Retrieve a list of sample answers.

## Installation

To install the Magic 8 Ball package, use `pip`:

```bash
pip install magic_eight_ball
```

## Usage

To use the package, import the functions you need:

```python
from magic_eight import get_questions, ask_question, shake_ball, get_answers

# Example usage
print(get_questions("en", 2))  # Get two sample questions in the given language
print(ask_question("fr"))      # Ask a random question and get an answer in the given language
print(shake_ball("en", 2))     # Shake the ball with a 2-second delay
print(get_answers("es", 3))    # Get three sample answers in the given language
```

## Functions

### `get_questions(language, count=0)`
Retrieve a list of sample questions in the specified language.

- **Parameters**:
  - `language` (str): The language code (e.g., "en" for English).
  - `count` (int, optional): Number of questions to return. Default is 0, which returns all questions.

- **Returns**: `list` of questions.

#### Example
```python
get_questions("en", 2)
# Output: ["Will I have a good day today?", "Should I go for that job interview?"]
```

### `ask_question(language, question="")`
Ask a question and get a random answer.

- **Parameters**:
  - `language` (str): The language code.
  - `question` (str, optional): A specific question to ask. If empty, a random question is generated.

- **Returns**: `tuple` of (question, answer).

#### Example
```python
ask_question("fr", "Vais-je atteindre mes objectifs cette année?")
# Output: ("Vais-je atteindre mes objectifs cette année?", "Oui, absolument!")
```

### `shake_ball(language, shake_time=10)`
Shake the ball to get another response to the previous question.

- **Parameters**:
  - `language` (str): The language code.
  - `shake_time` (int, optional): Time in seconds to simulate shaking. Default is 10.

- **Returns**: `str` answer.

#### Example
```python
shake_ball("es", 1)
# Output: "Sí."
```

### `get_answers(language, count=0)`
Retrieve a list of sample answers in the specified language.

- **Parameters**:
  - `language` (str): The language code.
  - `count` (int, optional): Number of answers to return. Default is 0, which returns all answers.

- **Returns**: `list` of answers.

#### Example
```python
get_answers("en", 3)
# Output: ["Yes, definitely!",  "It is certain.", "Without a doubt."]
```

## Running Tests

To run the unit tests for this package, use the following command:

```bash
PYTHONPATH=src python -m unittest discover -s src/tests
```

## Contribution Guidelines

If you’d like to contribute:

1. Clone the repository and create a new feature branch.
2. Make your changes in the feature branch.
3. Create a pull request to merge into the `main` branch.
4. Ensure all tests pass by running:
   ```bash
   PYTHONPATH=src python -m unittest discover -s src/tests
   ```
5. Your code will be reviewed, and if everything is in order, it will be merged.

### Developer Setup

- **Install dependencies**: Use `pipenv` to set up a virtual environment:
  ```bash
  pipenv install
  ```
- **Run tests with `pytest`**:
  ```bash
  pipenv run pytest
  ```
- **Build the package**:
  ```bash
  pipenv run python -m build
  ```
- **Upload to PyPI**:
  ```bash
  pipenv run twine upload dist/*
  ```

## Example Program

Below is an example script demonstrating the use of all functions in this package:

```python
from magic_eight import get_questions, ask_question, shake_ball, get_answers

# Get sample questions
print(get_questions("fr", 2))

# Ask a question
print(ask_question("en", "Will I get the internship?"))

# Shake the ball for a new answer
print(shake_ball("es", 1))

# Get sample answers
print(get_answers("en", 3))
```

## Contributors

- [Natalie Trump](https://github.com/nht251)
- [Alexandra Mastrangelo](https://github.com/alexandramastrangelo)

## Links

- [PyPI page for this package](https://pypi.org/project/magic-eight-ball/0.1.0/)
- [GitHub Repository](https://github.com/software-students-fall2024/3-python-package-magic-eight)