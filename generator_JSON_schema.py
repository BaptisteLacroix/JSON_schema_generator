import json
import re

from jsonschema import Draft7Validator

CONST_TYPE = {
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
    "list": "array",
    "dict": "object",
    "NoneType": "null",
}


def get_json_schema(json_data):
    schema = {
        "type": "object",
        "properties": {}
    }
    _id = str(input("Enter the id of the object: "))
    json_data = search_object_id(json_data, _id)
    parse_json_data(json_data, schema)
    schema = {
        "additionalProperties": schema
    }
    return schema


def beautify_print_json(json_data):
    print(json.dumps(json_data, indent=2))

def search_object_id(json_data, id):
    """
    Search an object that have the id
    example :
    {
	"elements":
        {
            "3505": {
            ...
            },
            "3506": {
            ...
            }
        }
    }

    id = 3505
    return the object with id 3505
    :param json_data:
    :return:
    """
    # Get the elements object
    elements = json_data["elements"]
    # Get the keys of the elements object
    keys = elements.keys()
    object_json = {}
    # Iterate over the keys
    for key in keys:
        if key == id:
            object_json = elements[key]
            break
    return object_json


def parse_json_data(data, parent_schema):
    """
    Parse the JSON data and generate the JSON Schema
    :param data:
    :param parent_schema:
    :return:
    """
    for key, value in data.items():
        if isinstance(value, dict):
            if key == 'style':
                schema_property = {
                    "type": "object",
                    "properties": {
                        "border_color": {"type": "string"},
                        "border_width": {"type": "string"},
                        "border_style": {"type": "string"},
                        "border_radius": {"type": "string"},
                        "border_shadow": {"type": "string"},
                        "header_size": {"type": "string"},
                        "header_align": {"type": "string"},
                        "header_color": {"type": "string"},
                        "header_background": {"type": "string"},
                        "header_weight": {"type": "string"},
                        "content_theme": {"type": "string"},
                        "background_blur": {"type": "string"},
                        "pins": {"type": "string"},
                        "background_opacity": {"type": "string"},
                    },
                }
            else:
                schema_property = {"type": "object", "properties": {}}
                parent_schema["properties"][key] = schema_property
                parse_json_data(value, schema_property)
        elif isinstance(value, list):
            if value:
                first_element = value[0]
                if isinstance(first_element, dict):
                    schema_property = {
                        "type": "array",
                        "items": {"type": "object", "properties": {}},
                    }
                    parent_schema["properties"][key] = schema_property
                    parse_json_data(first_element, schema_property["items"])
                else:
                    schema_property = {
                        "type": "array",
                        "items": {"type": CONST_TYPE[type(first_element).__name__]},
                    }
                    parent_schema["properties"][key] = schema_property
            else:
                schema_property = {"type": "array"}
                parent_schema["properties"][key] = schema_property
        else:
            schema_property = {"type": CONST_TYPE[type(value).__name__]}
            parent_schema["properties"][key] = schema_property
        # Assign the schema property to the parent schema for the current key
        parent_schema["properties"][key] = schema_property


def read_readme_file():
    with open("README.md", "r") as f:
        return f.read()


def write_readme_file(content):
    with open("README.md", "w") as f:
        f.write(content)


def insert_json_schema(schema_title, json_schema, readme_content):
    # Find the position of the last "TODO" section
    todo_pattern = r"(?s)(## TODO.*?)(##.*)"
    match = re.search(todo_pattern, readme_content)
    new_readme_content = readme_content
    if match:
        start_pos, end_pos = match.span(1)
        new_readme_content = (
                readme_content[:start_pos] +
                f"## Widget {schema_title}\n```json\n" +
                json.dumps(json_schema, indent=2) +
                "\n```\n\n## TODO\n\n\n" +
                readme_content[end_pos:]
        )
    return new_readme_content


def main():
    input_file = "export.json"  # Replace with your JSON file path

    with open(input_file, "r") as f:
        json_data = json.load(f)

    json_schema = get_json_schema(json_data)

    # Optionally, validate the JSON against the generated schema
    validator = Draft7Validator(json_schema)
    for error in validator.iter_errors(json_schema):
        print("Validation Error:", error)

    # Read the README.md file
    readme_content = read_readme_file()

    schema_title = str(input("Enter the title of the JSON Schema: "))
    # Insert the JSON Schema at the appropriate position
    new_readme_content = insert_json_schema(schema_title, json_schema, readme_content)

    # Write the updated README.md file
    write_readme_file(new_readme_content)

if __name__ == "__main__":
    main()
