import json

def count_third_level(data):
    count = 0
    for value in data.values():
        if isinstance(value, dict):
            for inner_value in value.values():
                if isinstance(inner_value, dict):
                    count += len(inner_value)
    return count

with open('tree.json', 'r') as json_file:
    json_data = json.load(json_file)

third_level_count = count_third_level(json_data)
print("Number of elements at least three levels deep:", third_level_count)