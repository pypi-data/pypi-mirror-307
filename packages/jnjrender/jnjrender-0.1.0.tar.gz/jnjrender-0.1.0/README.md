# jnjrender

**jnjrender** is a Python command-line application designed to render [Jinja2](https://jinja.palletsprojects.com/) templates into YAML files using variables from a specified YAML file. It allows for flexible templating by combining the power of Jinja2 and YAML, making it easy to create complex YAML configurations with dynamic content.

## Features

- Render Jinja2 templates with values from a YAML file.
- Output rendered content to the console or save it to a file.
- Simple command-line interface for ease of use.

## Installation

Clone this repository and install the requirements:

```bash
git clone https://github.com/yourusername/jnjrender.git
cd jnjrender
pip install -r requirements.txt
```

## Examples

```bash
python jnjrender.py template.j2 variables.yaml --output output.yaml
## prints stdout
python jnjrender.py template.j2 variables.yaml

```
