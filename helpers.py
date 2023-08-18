import yaml

CONFIG = 'configs/checkbox_data_methods.yaml'


def load_yaml(path=CONFIG):
    with open(path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data


def save_yaml(data, path=CONFIG):
    with open(path, 'w') as yaml_file:
        yaml.safe_dump(data, yaml_file)


if __name__ == '__main__':
    data = load_yaml()
    print(data)
