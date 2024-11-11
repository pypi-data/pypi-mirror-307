import argparse
import yaml
from jinja2 import Template

def render_jinja_to_yaml(jinja_file, yaml_file, output_file=None):
    # Load Jinja2 template
    with open(jinja_file) as file:
        template_content = file.read()
    template = Template(template_content)
    
    # Load YAML variables
    with open(yaml_file) as file:
        variables = yaml.safe_load(file)
    
    # Render template with variables
    rendered_content = template.render(variables)
    
    # Output to file or stdout
    if output_file:
        with open(output_file, 'w') as file:
            file.write(rendered_content)
            print(f"* generated {output_file}")

    else:
        print(rendered_content)

def main():
    parser = argparse.ArgumentParser(description="Render a Jinja2 file with YAML variables.")
    parser.add_argument("jinja_file", help="Path to the Jinja2 template file.")
    parser.add_argument("yaml_file", help="Path to the YAML file with variables.")
    parser.add_argument("--output", "-o", help="File to write rendered output. Prints to stdout if not specified.")
    
    args = parser.parse_args()
    render_jinja_to_yaml(args.jinja_file, args.yaml_file, args.output)
    
if __name__ == "__main__":
    main()
