# pylint: disable-msg=C0103
# pylint: disable-msg=C0411
# pylint: disable-msg=E0401

import os
import re
import yaml

from dotenv import load_dotenv
from .logging.logger import Log

log = Log(__name__)

path_matcher = re.compile(r'\$\{([^}^{]+)\}')


def path_constructor(_, node):
    ''' Extract the matched value, expand env variable, and replace the match '''
    value = node.value
    match = path_matcher.findall(value)  # to find all env variables in line
    full_value = value
    for g in match:
        full_value = full_value.replace(f'${{{g}}}', os.getenv(g, os.getenv(f'DEFAULT_{g}', f'NOT_FOUND_{g}')))
    return full_value


yaml.add_implicit_resolver('!path', path_matcher, None, yaml.SafeLoader)
yaml.add_constructor('!path', path_constructor, yaml.SafeLoader)


def config_loader(default_file="config.yaml"):
    log.debug(f"Loading config file: {default_file}")
    load_dotenv()
    file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', default_file)
    with open(file, 'rt', encoding='utf-8') as f:
        return yaml.safe_load(f.read())
