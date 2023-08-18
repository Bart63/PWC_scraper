import json
import yaml

output_file = 'configs/checkbox_data_sota.yaml'

with open('data/tree_sota.json', 'r') as json_file:
    json_data = json.load(json_file)

yaml_data = []
for category_name, subcategories in json_data.items():
    category = {
        "name": category_name,
        "state": True,
        "hasRead": False,
        "subcategories": []
    }
    for subcategory_name, tasks in subcategories.items():
        subcategory = {
            "name": subcategory_name,
            "state": False,
            "hasRead": False,
            "tasks": []
        }
        for task_name, task_href in tasks.items():
            task = {
                "name": task_name,
                "href": task_href,
                "hasRead": False,
                "state": True
            }
            subcategory["tasks"].append(task)
        category["subcategories"].append(subcategory)
    yaml_data.append(category)

with open(output_file, 'w') as yaml_file:
    yaml.dump({"categories": yaml_data}, yaml_file, default_flow_style=False)
