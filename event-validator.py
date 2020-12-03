import os
import json

# For cool features
from datetime import datetime
from difflib import SequenceMatcher


# Dictionary with representation of
# Python TYPES as JSON TYPES
TYPES = {
    dict: 'object',
    list: 'array',
    int: 'integer',
    float: 'float',
    str: 'string',
    bool: 'boolean',
    type(None): 'null'
}


# Path to the folder with JSON schemas
PATH_SCHEMA = "/path/to/folder"

# Path to the folder with JSON files
PATH_JSON = "/path/to/folder"

# Path to save log file
PATH_LOG = "/path/to/file"


def similar(s, l):
    similarities = [
        SequenceMatcher(None, s, e).ratio() for e in l
    ]
    
    return tuple(l)[similarities.index(max(similarities))]


def validate(data, schema, step=1):
    prefix = "  " * step  # little beauty

    output = ""

    # Validate type
    if TYPES[type(data)] not in schema["type"]:

        # Formats output like this:
        #  - Type of this property is not "null" or "integer"!
        #
        # P.S: Yes, code lo+s awful -_-
        output += "\n{}- Type of this property is not {}!".format(
            prefix,
            ' or '.join(map(lambda s: "\"{}\"".format(s), schema["type"]))
            if type(schema["type"]) is list else "\"{}\"".format(schema["type"])
        )

        # Add actual type of the property
        output += "\n{}| Its actual type is \"{}\".".format(
            prefix, TYPES[type(data)]
        )

        # Also add value of the property if its type is
        # integer, float, string or boolean
        if type(data) not in (dict, list, type(None)):
            output += "\n{}| And its value is \"{}\".".format(
                prefix,
                data
            )

    # Validate data if its type is "object"
    if type(data) is dict:

        # Validate for the required properties, if any
        if 'required' in schema:
            for required in schema["required"]:
                if required not in data.keys():
                    output += "\n{}- Property \"{}\" is missing!".format(
                        prefix, required
                    )

            # Validate required properties
            for prop in data.keys():
                if prop in schema["required"]:
                    output_temp = validate(
                        data[prop],
                        schema["properties"][prop], step+1
                    )
                    
                    output += "\n{}  Validating \"{}\" property: {}".format(
                        prefix,
                        prop,
                        '+' if ' - ' not in output_temp else '-'
                    )
                    output += output_temp

    # Validate data if its type is "array"
    if type(data) is list:
        for i in range(len(data)):
            output_temp = validate(
                data[i], 
                schema['items'], step+1
            )

            output += "\n{}  Validating its {} item: {}".format(
                prefix,
                i+1,
                '+' if ' - ' not in output_temp else '-'
            )
            output += output_temp   

    return output


if __name__ == "__main__":
    # Load all JSON schemas
    schemas = {}
    for schema in os.listdir(PATH_SCHEMA):
        with open(os.path.join(PATH_SCHEMA, schema)) as file:
            schemas[os.path.splitext(schema)[0]] = json.load(file)

    # List all JSON files
    files = {file: None for file in sorted(os.listdir(PATH_JSON))}

    # Variables for output
    output = str(datetime.now())
    results = {}

    # Validate all JSON files
    for file in files.keys():
        output += "\n\nValidating event \"{}\":".format(
            os.path.splitext(file)[0]
        )

        # Mark file as valid for now
        results[file] = True

        # Try to load file
        try:
            with open(os.path.join(PATH_JSON, file)) as f:
                event = json.load(f)
        except IOError:
            output += " Invalid"
            output += "\n- File is broken!"
            results[file] = False
            continue
        else:
            if type(event) is not dict:
                output += " Invalid"
                output += "\n- Root element is not \"object\"."
                output += "\n| Its actual type is \"{}\"".format(
                    TYPES[type(event)]
                )
                results[file] = False
                continue
        
        # For saving validating results 
        # for "head" of the file
        output_head = str()

        # Read and check event type
        try:
            event_type = event["event"]
        except KeyError:
            output_head += "\n- \"event\" property is missing."
            results[file] = False
        else:
            if event_type not in schemas.keys():
                output_head += "\n- Unknown event type \"{}\".".format(event_type)
                output_head += "\n| Maybe you meant \"{}\"?".format(
                    similar(event_type, schemas.keys())
                )
                results[file] = False

        # Read data property
        try:
            data = event["data"]
        except KeyError:
            output_head += "\n- \"data\" property is missing."
            results[file] = False
        
        output_data = str()

        # Validate data
        if results[file]:
            output_data = validate(data, schemas[event_type])

            # If any validation error was found
            # then the file is invalid
            if ' - ' in output_data:
                output_data = "\n  Validating \"data\" property: -" + output_data
                results[file] = False
            else:
                output_data = "\n  Validating \"data\" property: +" + output_data

        # Concantenate all outputs
        output += " Valid" if results[file] else " Invalid"
        output += output_head
        output += output_data


    # Summary of the validation result

    # Total events
    output += "\n\n\nTotal events: {}".format(len(results))

    # Number and Name of Valid events
    output += "\n\nValid events ({}): ".format(
        list(results.values()).count(True)
    )

    for file, result in results.items():
        if result:
            output += "\n+ \"{}\"".format(os.path.splitext(file)[0])

    # Number and Names of Invalid events
    output += "\n\nInvalid events ({}): ".format(
        list(results.values()).count(False))

    for file, result in results.items():
        if not result:
            output += "\n- \"{}\"".format(os.path.splitext(file)[0])


    # THE END. :)
    with open(PATH_LOG, 'w') as file:
        file.write(output)
