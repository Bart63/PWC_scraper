import yaml

with open('configs/checkbox_data_template.yaml', 'r') as yaml_file:
    data = yaml.safe_load(yaml_file)

print(data)
