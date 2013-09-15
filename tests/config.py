import os
from configparser import ConfigParser, ExtendedInterpolation

TEST_DIR = os.path.abspath(os.path.dirname(__file__))

def get_config(verbose=False):
    if not verbose:
        def noprint(*args):
            pass
        print = noprint
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config_files = [
        os.path.join(TEST_DIR, 'defaults.cfg'), 
        os.path.abspath(os.path.join(TEST_DIR, 'local.cfg')),
        os.path.abspath(os.path.join(TEST_DIR, '..', 'local.cfg')),
    ]

    files = config.read(config_files)
    print('Read configuration from :')
    for f in files:
        print(f)
    print()

    for sec in config:
        print(sec)
        for v in config[sec]:
            print(v, config[sec][v])
    
    return config




