""" JSON validator """

from jsonschema import validate, ValidationError

schema = {
    "type" : "object",
    "properties" : {
        "title":  {"type" : "string"},
        "author": {"type" : "string"},
        "abstract": {"type" : "string"}
    },
    "required": ["title", "author", "abstract"]
}

def validate_input(input_data):
    try:
        validate(input_data, schema)
    except ValidationError as err:
        return (False, err.message)
    return (True, None)
