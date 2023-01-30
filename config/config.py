import json
import doctest


class Configuration:
    """
    Example of usage:

    >>> configuration = Configuration("config")

    >>> configuration.get("config", "developer.log")
    {'exceptions': True, 'errors': True, 'notices': True}
    >>> print("Name: ", configuration.get("config", "name"))
    Name:  Plan It
    """
    def __init__(self, *files):
        """
        Class for storing config data usage

        @param *files: Names of JSON files with configuration
        """
        self.file_template = "{}.json"
        self.saved = {}
        for name in files:
            self.__fetch(name)

    # noinspection PyTypeChecker
    def __fetch(self, name: str):
        """Fetches content of JSON file and load in to parameter

        @type name: str
        @param name: Name of configuration file to load, also name for category
        """

        file = self.file_template.format(name)
        try:
            with open(file, 'r') as c:
                content = json.load(c)
        except Exception as error:
            raise error
        self.saved[name] = {}
        for key, value in content.items():
            self.saved[name][key] = value

    # noinspection PyTypeChecker
    def get(self, category: str, key: str):
        """ Get provided key from selected category

        @type category: str
        @param category: Name of category
        @type key: str
        @param key: Key of specified value
        """
        config = self.saved[category]
        keys = key.split('.')
        try:
            for key in keys:
                config = config[key]
        except Exception as error:
            raise error
        return config


doctest.run_docstring_examples(Configuration, globals())
