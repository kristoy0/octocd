from octocd import configparser


class TestConfigParser:
    def test_parsing(self):
        config = """
        image: python:latest

        ports:
          - 8080:80
          - 8443:443

        install_it:
          - apt-get install python-pip
          - pip install -r requirements.txt

        build_it:
          - echo "build step"

        start_it:
          - python runserver.py

        test_it:
          - curl http://localhost:80
        """

        valid_dict = {
            'image':
            'python:latest',
            'ports': ['8080:80', '8443:443'],
            'install_it':
            ['apt-get install python-pip', 'pip install -r requirements.txt'],
            'build_it': ['echo "build step"'],
            'start_it': ['python runserver.py'],
            'test_it': ['curl http://localhost:80']
        }

        config_dict = configparser.validate_config(config)

        assert config_dict == valid_dict

    def test_parsing_fail(self):
        config = """
        image: python:latest

        install_it:
          - apt-get install python-pip
          - pip install -r requirements.txt

        start_it:
          - python runserver.py

        test_it:
          - curl http://localhost:5000
        """

        config_dict = configparser.validate_config(config)

        assert "Given YAML configuration is not valid:" in config_dict

    def test_config_script_creation(self):
        config = """
        image: python:latest

        ports:
          - 8080:80

        build_it:
          - echo "build step"

        install_it:
          - apt-get install python-pip
          - pip install -r requirements.txt

        start_it:
          - python runserver.py

        test_it:
          - curl http://localhost:5000
        """

        script = ('apt-get install python-pip && '
                  'pip install -r requirements.txt && '
                  'echo "build step" && '
                  'python runserver.py && '
                  'curl http://localhost:5000')

        config_metadata, config_script = configparser.create_config_script(
            config)

        assert config_metadata == {
            'image': 'python:latest',
            'ports': ['8080:80']
        }

        assert config_script == script
