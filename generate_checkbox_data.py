import json
import yaml

output_file = 'checkbox_data.yaml'

with open('tree.json', 'r') as json_file:
    json_data = json.load(json_file)

yaml_data = []
for category_name, subcategories in json_data.items():
    category = {
        "name": category_name,
        "state": True,
        "subcategories": []
    }
    for subcategory_name, tasks in subcategories.items():
        subcategory = {
            "name": subcategory_name,
            "state": True,
            "tasks": []
        }
        for task_name, task_href in tasks.items():
            task = {
                "name": task_name,
                "href": task_href,
                "state": True
            }
            subcategory["tasks"].append(task)
        category["subcategories"].append(subcategory)
    yaml_data.append(category)

with open(output_file, 'w') as yaml_file:
    yaml.dump({"categories": yaml_data}, yaml_file, default_flow_style=False)
