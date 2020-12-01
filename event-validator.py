import os
import json
import jsonschema

# For cool features
from datetime import datetime
from difflib import SequenceMatcher


# Path to the folder with JSON schemas
PATH_SCHEMA = "/home/shvix/Documents/Interviews/Welltory/task_folder/schema"

# Path to the folder with JSON files
PATH_JSON = "/home/shvix/Documents/Interviews/Welltory/task_folder/event"

# Path to save log file
PATH_LOG = "/home/shvix/Documents/Interviews/Welltory/task_folder/output.log"


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
    output += "\n\nValidating event \"{}\": [[result]]".format(
        os.path.splitext(file)[0])

    results[file] = True

    # Load file
    with open(os.path.join(PATH_JSON, file)) as f:
        event = json.load(f)

    if event is None:
        output += "\n- Event is empty (equals null)."
        results[file] = False
        continue

    # Read event type
    try:
        event_type = event["event"]
    except KeyError:
        output += "\n- \"event\" property is missing."
        results[file] = False
        continue

    # Check event type
    if event_type not in schemas.keys():
        output += "\n- Unknown event type \"{}\".".format(event_type)

        def similar():
            similarities = [SequenceMatcher(
                None, event_type, e).ratio() for e in schemas.keys()]
            return list(schemas.keys())[similarities.index(max(similarities))]

        output += "\n| Maybe you meant \"{}\"?".format(similar())
        results[file] = False
        continue

    # Validate data
    try:
        data = event["data"]
    except KeyError:
        output += "\n- \"data\" property is missing."
        results[file] = False
        continue

    # Dictionary with representation of
    # Python types as JSON types
    types = {
        dict: 'object',
        list: 'array',
        int: 'integer',
        float: 'float',
        str: 'string',
        bool: 'boolean',
        type(None): 'null'
    }

    def validate(data, schema, step=1):
        prefix = "  " * step  # little beauty

        output = ""

        # Validate type
        if types[type(data)] not in schema["type"]:

            # Formats output like this:
            #  - Type of this property is not "null" or "integer"!
            #
            # P.S: Yes, code looks awful -_-
            output += "\n{}- Type of this property is not {}!".format(
                prefix,
                ' or '.join(map(lambda s: "\"{}\"".format(s), schema["type"]))
                if type(schema["type"]) is list else schema["type"])

            # Add actual type of the property
            output += "\n{}| Its actual type is \"{}\".".format(
                prefix, types[type(data)])

        # Validate data if its type is "object"
        if type(data) is dict:

            # Validate for the required properties
            for required in schema["required"]:
                if required not in data.keys():
                    output += "\n{}- Property \"{}\" is missing!".format(
                        prefix, required)

            # Validate required properties
            for prop in data.keys():
                if prop in schema["required"]:
                    output += "\n{}  Validating \"{}\" property:".format(
                        prefix, prop)

                    output += validate(data[prop],
                                       schema["properties"][prop], step+1)

        # Validate data if its type is "array"
        if type(data) is list:
            for i in range(len(data)):
                # Just format number (1, 2, 3..)
                # with their ordinal representation (1st, 2nd, 3rd..)
                output += "\n{}  Validating its {} item:".format(
                    prefix,
                    "%d%s" % (i, "tsnrhtdd"[(i//10 % 10 != 1)*(i % 10 < 4)*i % 10::4]))  # little magic

                # Validate type of the item
                if types[type(data[i])] not in schema["type"]:
                    output += "\n{}- Type of this item is not {}!".format(
                        prefix, schema["type"])

                # Validate this item if its type is "object"
                elif type(data[i]) is dict:
                    output += validate(data[i], schema['items'], step+1)

        return output

    output += "\n  Validating \"data\" property:"
    output_validation = validate(data, schemas[event_type])

    # If a validation error was found
    # then the file is invalid
    if ' - ' in output_validation:
        results[file] = False

    output = output.replace('[[result]]', "Invalid" if results[file] is False else "Valid")

    output += output_validation


# Add amount and names of Valid events
output += "\n\n\nValid events ({}): ".format(
    list(results.values()).count(True))

for file, result in results.items():
    if result:
        output += "\n+ \"{}\"".format(os.path.splitext(file)[0])

# Add amount and names of Invalid events
output += "\n\nInvalid events ({}): ".format(
    list(results.values()).count(False))

for file, result in results.items():
    if not result:
        output += "\n- \"{}\"".format(os.path.splitext(file)[0])


# THE END. :)
with open(PATH_LOG, 'w') as file:
    file.write(output)    
