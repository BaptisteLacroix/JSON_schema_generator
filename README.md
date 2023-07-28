# JSON Schema Generator

### Overview

This script was created to address a specific need: generating JSON Schemas for a large number of JSON files, allowing users to modify the JSON data while adhering to the defined Schema. Additionally, it facilitates the process of documenting the Schemas by automatically inserting them into the README file.

### Motivation

The motivation behind developing this script was the requirement to provide users with a structured way to modify JSON data while ensuring its validity. Manually creating JSON Schemas and documenting them for each JSON file became impractical due to the sheer volume of files involved. Therefore, automating the process through this script significantly improved efficiency and reduced human error.

### Use Case

The script takes a JSON file as input, prompts the user to enter an object ID from the JSON data, and generates a JSON Schema based on the structure of the selected object. The generated JSON Schema serves as a blueprint for the JSON data, specifying the expected properties and data types. This ensures that any modifications made by users conform to the prescribed Schema.

### Benefits

1. **Efficiency**: The script automates the generation of JSON Schemas, saving time and effort when dealing with numerous JSON files.

2. **Validation**: The generated JSON Schemas help validate user-modified JSON data, preventing inconsistencies and errors.

3. **Documentation**: By inserting the generated JSON Schemas into the README file, the script enhances documentation and provides a clear reference for users.

4. **Consistency**: Using JSON Schemas ensures that all modified JSON data follows the same structure, promoting consistency throughout the project.

5. **User-Friendly**: Users can confidently modify JSON data, knowing that the changes align with the Schema's specifications.

6. **Scalability**: The script can handle a large number of JSON files efficiently, making it scalable for projects with varying sizes and complexities.

### Utility

The script takes a JSON file (`export.json` by default) as input and prompts the user to enter an object ID from the JSON data. It then extracts the object with the provided ID and generates a JSON Schema based on its structure. AFter that the JSON Schema is saved in a JSON file (`ouput_schema.json` by default).

The JSON Schema is designed to describe the expected properties and data types of the objects within the JSON data. It supports the following data types:

- `"string"`: Represents a string.
- `"integer"`: Represents an integer number.
- `"number"`: Represents a floating-point number.
- `"boolean"`: Represents a boolean value (`True` or `False`).
- `"array"`: Represents a list of items.
- `"object"`: Represents a nested JSON object.
- `"null"`: Represents a null value.

The generated JSON Schema is then inserted into the `README.md` file, under a section with a user-defined title.

### How to Run

1. Make sure you have Python installed on your system.

2. Install the required Python libraries by running the following command in your terminal or command prompt:

   ```
   pip install jsonschema
   ```

3. Save your JSON data in a file named `export.json` in the same directory as this script. If your data is in a different file, modify the `input_file` variable in the `main()` function to point to your JSON file.

4. Run the script by executing the following command:

   ```
   python script_name.py
   ```

5. The script will prompt you to enter the ID of the object you want to use as the basis for generating the JSON Schema.

6. Next, the script will generate the JSON Schema and validate it against the provided JSON data using the `jsonschema` library. Any validation errors, if found, will be printed to the console.

7. After successful execution, the script will update the `README.md` file with the generated JSON Schema, placed under a section titled with a user-defined title.

8. The updated `README.md` file will contain the generated JSON Schema in a formatted manner for easy reference.

**Note:** Ensure that the `README.md` file exists in the same directory as the script before running it.

**Important:** It is recommended to back up your `README.md` file before running the script, especially if it contains important content, as the script will modify it during execution.

**Disclaimer:** This script relies on the assumption that the provided JSON data is properly structured and contains the required object with the specified ID. Any inconsistencies in the JSON data may lead to unexpected behavior or errors in the script.

For more information on JSON Schema, refer to the [JSON Schema Documentation](https://json-schema.org/).
