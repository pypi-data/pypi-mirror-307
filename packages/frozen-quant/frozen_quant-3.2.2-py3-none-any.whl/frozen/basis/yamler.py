import yaml
import os

class yamler:
    
    def __init__(self, yaml_path):
        if not os.path.isfile(yaml_path):
            raise FileNotFoundError(f'File not exist, please check if path is correct: {yaml_path}')
        self.yaml_path = yaml_path

    def get_yaml_fields(self, fields):
        with open(self.yaml_path, 'r') as file:
            yaml_data = yaml.load(file, Loader=yaml.FullLoader)
            result = []
            for field in fields:
                result.append(yaml_data.get(field))
        return result

    def get_all_fields(self):
        with open(self.yaml_path, 'r') as file:
            return yaml.safe_load(file.read())


