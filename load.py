import yaml

with open('checkbox_data.yaml', 'r') as yaml_file:
    data = yaml.safe_load(yaml_file)

print(data)
