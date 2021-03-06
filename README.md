# event-validator

Small script for validating JSON files with schemas.

## Usage

Change paths inside the script:

```python
# Path to the folder with JSON schemas
PATH_SCHEMA = "/path/to/folder"

# Path to the folder with JSON files
PATH_JSON = "/path/to/folder"

# Path to save log file
PATH_LOG = "/path/to/file"
```

Run the script:

```bash
python event-validator.py
```

## Example

```log
2020-12-04 01:07:35.368135

Validating event "1eba2aa1-2acf-460d-91e6-55a8c3e3b7a3": Invalid
  Validating "data" property: -
  - Property "unique_id" is missing!
  - Property "user" is missing!
  - Property "user_id" is missing!
    Validating "id" property: +
    Validating "rr_id" property: +
    Validating "labels" property: +
      Validating its 1 item: +
        Validating "slug" property: +
        Validating "type" property: +
        Validating "color" property: +
        Validating "name_en" property: +
        Validating "name_ru" property: +
        Validating "category" property: +
        Validating "type_stress" property: +
        Validating "is_custom_tag" property: +
        Validating "property_where" property: +
        Validating "property_arousal" property: +
        Validating "property_pleasure" property: +
        Validating "property_vitality" property: +
        Validating "property_stability" property: +
    Validating "timestamp" property: +

Validating event "297e4dc6-07d1-420d-a5ae-e4aff3aedc19": Valid
  Validating "data" property: +
    Validating "source" property: +
    Validating "timestamp" property: +
    Validating "unique_id" property: +
    Validating "time_start" property: +
    Validating "finish_time" property: +
    Validating "activity_type" property: +

Validating event "29f0bfa7-bd51-4d45-93be-f6ead1ae0b96": Invalid
- Root element is not "object".
| Its actual type is "null"

Validating event "2e8ffd3c-dbda-42df-9901-b7a30869511a": Invalid
- Unknown event type "meditation_created".
| Maybe you meant "cmarker_created"?

Validating event "3ade063d-d1b9-453f-85b4-dda7bfda4711": Invalid
- Unknown event type "cmarker_calculated".
| Maybe you meant "cmarker_created"?

Validating event "3b4088ef-7521-4114-ac56-57c68632d431": Valid
  Validating "data" property: +
    Validating "user_id" property: +
    Validating "cmarkers" property: +
    Validating "datetime" property: +

Validating event "6b1984e5-4092-4279-9dce-bdaa831c7932": Invalid
- Unknown event type "meditation_created".
| Maybe you meant "cmarker_created"?

Validating event "a95d845c-8d9e-4e07-8948-275167643a40": Invalid
- "event" property is missing.
- "data" property is missing.

Validating event "ba25151c-914f-4f47-909a-7a65a6339f34": Invalid
- Unknown event type "label_       selected".
| Maybe you meant "label_selected"?

Validating event "bb998113-bc02-4cd1-9410-d9ae94f53eb0": Invalid
  Validating "data" property: -
  - Property "unique_id" is missing!
    Validating "source" property: +
    Validating "timestamp" property: +
    Validating "time_start" property: +
    Validating "finish_time" property: +
    Validating "activity_type" property: +

Validating event "c72d21cf-1152-4d8e-b649-e198149d5bbb": Invalid
- Unknown event type "meditation_created".
| Maybe you meant "cmarker_created"?

Validating event "cc07e442-7986-4714-8fc2-ac2256690a90": Invalid
  Validating "data" property: -
  - Type of this property is not "object"!
  | Its actual type is "null".

Validating event "e2d760c3-7e10-4464-ab22-7fda6b5e2562": Invalid
  Validating "data" property: -
    Validating "user_id" property: -
    - Type of this property is not "integer"!
    | Its actual type is "string".
    | And its value is "bad user id".
    Validating "cmarkers" property: +
      Validating its 1 item: +
        Validating "id" property: +
        Validating "date" property: +
        Validating "slug" property: +
      Validating its 2 item: +
        Validating "id" property: +
        Validating "date" property: +
        Validating "slug" property: +
    Validating "datetime" property: +

Validating event "f5656ff6-29e1-46b0-8d8a-ff77f9cc0953": Valid
  Validating "data" property: +
    Validating "source" property: +
    Validating "timestamp" property: +
    Validating "unique_id" property: +
    Validating "time_start" property: +
    Validating "finish_time" property: +
    Validating "activity_type" property: +

Validating event "fb1a0854-9535-404d-9bdd-9ec0abb6cd6c": Invalid
  Validating "data" property: -
  - Property "cmarkers" is missing!
    Validating "user_id" property: +
    Validating "datetime" property: +

Validating event "ffe6b214-d543-40a8-8da3-deb0dc5bbd8c": Invalid
  Validating "data" property: -
    Validating "user_id" property: -
    - Type of this property is not "integer"!
    | Its actual type is "null".
    Validating "cmarkers" property: -
    - Type of this property is not "array"!
    | Its actual type is "string".
    | And its value is "suprt marker".
    Validating "datetime" property: +


Total events: 16

Valid events (3): 
+ "297e4dc6-07d1-420d-a5ae-e4aff3aedc19"
+ "3b4088ef-7521-4114-ac56-57c68632d431"
+ "f5656ff6-29e1-46b0-8d8a-ff77f9cc0953"

Invalid events (13): 
- "1eba2aa1-2acf-460d-91e6-55a8c3e3b7a3"
- "29f0bfa7-bd51-4d45-93be-f6ead1ae0b96"
- "2e8ffd3c-dbda-42df-9901-b7a30869511a"
- "3ade063d-d1b9-453f-85b4-dda7bfda4711"
- "6b1984e5-4092-4279-9dce-bdaa831c7932"
- "a95d845c-8d9e-4e07-8948-275167643a40"
- "ba25151c-914f-4f47-909a-7a65a6339f34"
- "bb998113-bc02-4cd1-9410-d9ae94f53eb0"
- "c72d21cf-1152-4d8e-b649-e198149d5bbb"
- "cc07e442-7986-4714-8fc2-ac2256690a90"
- "e2d760c3-7e10-4464-ab22-7fda6b5e2562"
- "fb1a0854-9535-404d-9bdd-9ec0abb6cd6c"
- "ffe6b214-d543-40a8-8da3-deb0dc5bbd8c"
```