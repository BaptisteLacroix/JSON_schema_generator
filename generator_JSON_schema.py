import json
import re
from re import Match

from jsonschema import Draft7Validator

CONST_TYPE: dict = {
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
    "list": "array",
    "dict": "object",
    "NoneType": "null",
}


def get_json_schema(json_data: dict) -> dict:
    """
    Generate a JSON Schema for the given JSON data.

    Args:
        json_data (dict): The JSON data to generate the schema for.

    Returns:
        dict: The generated JSON Schema.

    :param json_data: The JSON data to generate the schema for.
    :type json_data: dict
    :return: The generated JSON Schema.
    :rtype: dict
    """
    schema: dict = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {}
    }
    _id: str = str(input("Enter the id of the object: "))
    json_data: dict = search_object_id(json_data, _id)
    parse_json_data(json_data, schema)
    schema: dict = {
        "additionalProperties": schema
    }
    return schema


def beautify_print_json(json_data: dict) -> None:
    """
    Beautify print the given JSON data.

    Args:
        json_data (dict): The JSON data to print.

    Returns:
        None

    :param json_data: The JSON data to print.
    :type json_data: dict
    :return: None
    :rtype: None
    """
    print(json.dumps(json_data, indent=2))


def search_object_id(json_data: dict, id: str) -> dict:
    """
    Search an object with the given ID in the JSON data.

    Args:
        json_data (dict): The JSON data to search in.
        id (str): The ID of the object to find.

    Returns:
        dict: The object with the given ID, if found.

    :param json_data: The JSON data to search in.
    :type json_data: dict
    :param id: The ID of the object to find.
    :type id: str
    :return: The object with the given ID, if found.
    :rtype: dict
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


def parse_json_data(data: dict, parent_schema: dict) -> None:
    """
    Parse the JSON data and generate the JSON Schema.

    Args:
        data (dict): The JSON data to parse.
        parent_schema (dict): The parent schema to attach the generated schema to.

    Returns:
        None

    :param data: The JSON data to parse.
    :type data: dict
    :param parent_schema: The parent schema to attach the generated schema to.
    :type parent_schema: dict
    :return: None
    :rtype: None
    """
    for key, value in data.items():
        if isinstance(value, dict):
            schema_property = isinstance_of_dict(key, parent_schema, value)
        elif isinstance(value, list):
            schema_property = isinstance_of_list(key, parent_schema, value)
        else:
            schema_property = {"type": CONST_TYPE[type(value).__name__]}
            parent_schema["properties"][key] = schema_property
        # Assign the schema property to the parent schema for the current key
        parent_schema["properties"][key] = schema_property


def isinstance_of_dict(key: str, parent_schema: dict, value: dict) -> dict:
    """
    Check if the value is a dictionary and generate the corresponding JSON Schema property.

    Args:
        key (str): The key of the dictionary in the parent JSON Schema.
        parent_schema (dict): The parent JSON Schema to attach the generated property to.
        value (dict): The dictionary value to process.

    Returns:
        dict: The generated JSON Schema property.

    :param key: The key of the dictionary in the parent JSON Schema.
    :type key: str
    :param parent_schema: The parent JSON Schema to attach the generated property to.
    :type parent_schema: dict
    :param value: The dictionary value to process.
    :type value: dict
    :return: The generated JSON Schema property.
    :rtype: dict
    """
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
    return schema_property


def isinstance_of_list(key: str, parent_schema: dict, value: list) -> dict:
    """
    Check if the value is a list and generate the corresponding JSON Schema property.

    Args:
        key (str): The key of the list in the parent JSON Schema.
        parent_schema (dict): The parent JSON Schema to attach the generated property to.
        value (list): The list value to process.

    Returns:
        dict: The generated JSON Schema property.

    :param key: The key of the list in the parent JSON Schema.
    :type key: str
    :param parent_schema: The parent JSON Schema to attach the generated property to.
    :type parent_schema: dict
    :param value: The list value to process.
    :type value: list
    :return: The generated JSON Schema property.
    :rtype: dict
    """
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
    return schema_property


def read_readme_file(path_to_file: str = "./README.md") -> str:
    """
    Read the content of the specified file.

    Args:
        path_to_file (str, optional): The path to the file to read. Defaults to "./README.md".

    Returns:
        str: The content of the file.

    :param path_to_file: The path to the file to read.
    :type path_to_file: str
    :return: The content of the file.
    :rtype: str
    """
    with open(path_to_file, "r") as f:
        return f.read()


def write_readme_file(content: str, path_to_file: str = "./README.md") -> None:
    """
    Write the given content to the specified file.

    Args:
        content (str): The content to write to the file.
        path_to_file (str, optional): The path to the file to write. Defaults to "./README.md".

    Returns:
        None

    :param content: The content to write to the file.
    :type content: str
    :param path_to_file: The path to the file to write.
    :type path_to_file: str
    :return: None
    :rtype: None
    """
    with open(path_to_file, "w") as f:
        f.write(content)


def insert_json_schema(schema_title: str, json_schema: dict, readme_content: str) -> str:
    """
    Insert the generated JSON Schema into the README.md file.

    Args:
        schema_title (str): The title of the JSON Schema.
        json_schema (dict): The JSON Schema to insert.
        readme_content (str): The content of the README.md file.

    Returns:
        str: The updated content of the README.md file.

    :param schema_title: The title of the JSON Schema.
    :type schema_title: str
    :param json_schema: The JSON Schema to insert.
    :type json_schema: dict
    :param readme_content: The content of the README.md file.
    :type readme_content: str
    :return: The updated content of the README.md file.
    :rtype: str
    """
    # Find the position of the last "TODO" section
    todo_pattern: str = r"(?s)(## TODO.*?)(##.*)"
    match: Match[str] | None = re.search(todo_pattern, readme_content)
    new_readme_content: str = readme_content
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
    output_file = "output_schema.json"  # Replace with the desired output JSON Schema file path

    with open(input_file, "r") as f:
        json_data = json.load(f)

    json_schema = get_json_schema(json_data)

    with open(output_file, "w") as f:
        json.dump(json_schema, f, indent=2)

    # Optionally, validate the JSON against the generated schema
    validator = Draft7Validator(json_schema)
    for error in validator.iter_errors(json_schema):
        print("Validation Error:", error)

    print("JSON Schema generated and saved to:", output_file)

    # Read the README.md file
    readme_content = read_readme_file()

    schema_title = str(input("Enter the title of the JSON Schema: "))
    # Insert the JSON Schema at the appropriate position
    new_readme_content = insert_json_schema(schema_title, json_schema, readme_content)

    # Write the updated README.md file
    write_readme_file(new_readme_content)


if __name__ == "__main__":
    main()
