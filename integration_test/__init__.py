import os

import json

import jsonschema
from jsonschema import (Draft4Validator)


def validate_v0(json_string, schema_filename):
    schema_dir = os.path.join(os.path.dirname(__file__), 'schemas/v0')
    resolver = jsonschema.RefResolver('file://' + schema_dir + '/', None)
    with open(os.path.join(schema_dir, schema_filename)) as schema:
        jsonschema.validate(
            json_string,
            json.load(schema),
            format_checker=jsonschema.FormatChecker(),
            resolver=resolver
        )


def validate(json_to_validate, schema):
    validator = Draft4Validator(schema)
    validator.validate(json_to_validate, schema)
