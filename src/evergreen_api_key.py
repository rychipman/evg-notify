import os
import sys
import yaml

def _get_file_in_home_dir(filename):
    '''Generates the full path to a file in the user\'s home directory.
    
    `filename` - the name of the file.
    
    Returns the path as a string.
    '''
    return '{}/{}'.format(os.path.expanduser('~'), filename)

def get_evergreen_api_key(config_file=_get_file_in_home_dir('.evergreen.yml')):
    '''Parses the Evergeen API key from the user\'s config file.
    
    `config_file` - location of the user\'s Evergreen config file

    Returns the API key as a string.
    '''
    try:
        with open(config_file, 'r') as stream:
            config = yaml.load(stream)

            return config['api_key']
    except Exception as e:
        sys.stderr.write('''Error in reading Evergreen config file. Are you sure you specified the right location?\n''')
        sys.exit(1)

