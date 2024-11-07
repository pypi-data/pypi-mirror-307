import sys
from configparser import ConfigParser
import importlib
from unidecode import unidecode
import traceback

sys.path.append('eazyml/ez_explain')


def apply_unidecoding(object):
    """
    Recursively unidecode all unicode types
    """
    try:
        if isinstance(object, unicode):
            return unidecode(object)
        if isinstance(object, str):
            try:
                return unidecode(object.decode("utf-8"))
            except:
                try:
                    return unidecode(object.decode("utf-8", "ignore"))
                except:
                    return unidecode(object.encode("ascii", "ignore").decode(
                        "ascii", "ignore"))
        if isinstance(object, dict):
            for key in object:
                object[key] = apply_unidecoding(object[key])
        if isinstance(object, list):
            for i, o in enumerate(object):
                object[i] = apply_unidecoding(o)
        if isinstance(object, float) or isinstance(object, int):
            object = str(object)
    except Exception as e:
        traceback.print_exc()
    return object


class config_global_var(object):
    '''
        This class sets the context to global variables used by globals.py
        If the context is set by the filename, then variables
        given in that file will be given priority
        then the globals.py
    '''
    def __init__(self, filename=None):
        self.variables = []
        if filename is not None:
            self.filename = filename
            self.parser = ConfigParser()
            self.parser.read(self.filename)
            self.config_json = {}
            for section in self.parser.sections():
                options = self.parser.options(section)
                options_decoded = apply_unidecoding(options)
                for x in map(str.upper, options_decoded):
                    self.config_json[x] = section
                    self.variables.append(x)
        self.module = importlib.import_module('global_var')

    def __getattribute__(self, item):
        #first check if it's one of these things
        if item in ['filename','parser','config_json','module', 'variables']:
            return object.__getattribute__(self, item)
        #First check if config_json exists
        result = getattr(self.module, item, None)
        if result is not None and (isinstance(result, (
            int, float, complex)) or isinstance(
            result, bool)) and hasattr(self, 'config_json'):
            #check if it's mentioned in the config file
            if item.upper() in self.config_json:
                section_name = self.config_json[item]
                variable_name = item
                try:
                    if isinstance(result, bool):
                        config_result = self.parser.getboolean(
                            section_name, variable_name)
                    elif isinstance(result, (int)):
                        config_result = self.parser.getint(
                            section_name, variable_name)
                    elif isinstance(result, float):
                        config_result = self.parser.getfloat(
                            section_name, variable_name)
                    else:
                        config_result = None
                except ValueError as e:
                    config_result = None
                result = config_result
        return result


g = config_global_var() 

