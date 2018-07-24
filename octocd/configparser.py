import yaml
from jsonschema import validate, ValidationError

schema = {
    "type": "object",
    "properties": {
        "image": {
            "type": "string"
        },
        "ports": {
            "type": "array"
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
        return 'Given YAML configuration is not valid: {}'.format(e)

    return config_dict


def create_config_script(config):
    config_dict = validate_config(config)

    metadata = {
        'image': config_dict['image'],
        'ports': config_dict['ports']
    }

    script_array = config_dict['install_it'] + config_dict['build_it'] + config_dict['start_it'] + config_dict['test_it']

    script = ' && '.join(script_array)

    return metadata, script
