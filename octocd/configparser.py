import yaml
from jsonschema import validate, ValidationError

schema = {
    "type": "object",
    "properties": {
        "image": {
            "type": "string"
        },
        "install_it": {
            "type": "array"
        },
        "build_it": {
            "type": "array"
        },
        "start_it": {
            "type": "array"
        },
        "test_it": {
            "type": "array"
        },
    },
    "required": ["image", "install_it", "build_it", "start_it", "test_it"]
}


def parse_yaml(config):
    """Safely loads yaml data

    Args:
        config: YAML configuration file

    Returns:
        Dictionary representation of given YAML
    """
    return yaml.safe_load(config)


def validate_config(config):
    """Validates configuration

    Validates YAML configuration according to
    JSON schema

    Args:
        config: YAML configuration file

    Returns:
        Dictionary representation of given YAML
        if it is valid
    """
    config_dict = parse_yaml(config)
    try:
        validate(config_dict, schema)
    except ValidationError as e:
        return "Given YAML configuration is not valid: {}".format(e)

    return config_dict
