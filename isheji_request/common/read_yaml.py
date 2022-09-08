import yaml
import os
from common.path_config import config_position

def read_yaml(file):
    with open(file, encoding='utf-8') as f:
        wenjian = yaml.safe_load(f)
        return wenjian

yaml_read = read_yaml(os.path.join(config_position, '../config/login.yaml'))
url = yaml_read["url"]
username = yaml_read['username']
password = yaml_read['password']

api_read = read_yaml(os.path.join(config_position, '../config/url.yaml'))
api_url = api_read['url']
