from yta_general_utils.file.writer import FileWriter
from yta_general_utils.file.reader import FileReader
from yta_general_utils.programming.path import get_project_abspath

import json


CONFIG_MANIM_ABSPATH = get_project_abspath() + 'manim_parameters.json'

class ManimConfig:
    @classmethod
    def write(cls, json_data):
        """
        Writes the the provided 'json_data' manim configuration
        in the configuration file so the parameters could be read
        later by the manim engine. This is the way to share 
        parameters to the process.
        """
        # TODO: Check that 'json_data' is valid and well-formatted
        FileWriter.write_file(json.dumps(json_data, indent = 4), CONFIG_MANIM_ABSPATH)

    @classmethod
    def read(cls):
        """
        Read the configuration file and return it as a json
        object.
        """
        return FileReader.read_json_from_file(CONFIG_MANIM_ABSPATH)



# TODO: Remove this below when unneded
def write_manim_config_file(json_data):
    """
    Writes in the configuration file that we use to share
    parameters with manim software. This is the way to 
    share parameters to the process.
    
    TODO: I would like to be able to handle manim through 
    python code directly and not an external process I run,
    but for now this is working.
    """
    # We serialize json to str
    json_object_str = json.dumps(json_data, indent = 4)
    
    FileWriter.write_file(json_object_str, CONFIG_MANIM_ABSPATH)

def read_manim_config_file():
    """
    Reads the configuration file and returns it as a json
    object.
    """
    return FileReader.read_json_from_file(CONFIG_MANIM_ABSPATH)