import os
import json
import jsonschema

from difflib import SequenceMatcher


# Path to the folder with JSON schemas
PATH_SCHEMA = "/home/shvix/Documents/Interviews/Welltory/task_folder/schema"

# Path to the folder with JSON files
PATH_JSON = "/home/shvix/Documents/Interviews/Welltory/task_folder/event"


# Load all JSON schemas
schemas = {os.path.splitext(schema)[0]: json.loads(schema) for schema in os.listdir(PATH_SCHEMA)}

# List all JSON files
files = {file: None for file in os.listdir(PATH_JSON)}


output = ""

# Validate schemas
for schema, file in schemas:
    try:
        jsonschema.Draft3Validator.check_schema(file)
    except jsonschema.exceptions.SchemaError as e:
        output += "\nSchema \"{}\" is invalid!".format(schema)
        output += "\n - {}".format(e.message)
        schemas[schema] = None


# Validate all JSON files
for file in files.keys():
    output += "\n\nValidating event {}".format(file)

    try:
        # Load files
        event = json.loads(file)

        # Read event type
        try:
            event_type = event["event"]
        except KeyError:
            output += "\n - \"event\" attribute is missing."
            break
        
        # Check event type
        if event_type not in schemas.keys():
            output += "\n - Unknown event type \"{}\".".format(event_type)

            similar = schemas.keys()[max(SequenceMatcher(None, event_type, e) for e in schemas.keys())]

            output += "\n   Maybe you meant \"{}\"?".format(similar)
            break
        
        # Validate JSON file
        if schemas[event_type] is None:
            output += "\n - Cannot validate event because schema \"{}\" is Invalid.".format(event_type)
        else:
            validator = jsonschema.Draft3Validator(schemas[event_type])

            for e in validator.iter_errors(file):
                output += "\n - {}".format(e.message)

    except ValueError as e:
        output += "\n - {}".format(e)
    
    if files[file] is None:
        files[file] = True

