import json
from typing import List, Any
import os
import sys
from copy import deepcopy


def get_data_folder() -> str:
    root_folder = os.path.dirname(sys.modules['__main__'].__file__)
    data_folder = f'{root_folder}/data'
    os.makedirs(data_folder, exist_ok=True)
    return data_folder


def load_json_list(file_path: str) -> List[dict]:
    json_list: List[dict] = []
    if os.path.exists(file_path):
        f = open(file_path)
        # returns JSON object as
        # a dictionary
        json_list = json.load(f)
        f.close()
    return json_list


def filter_obj(json_obj: dict, filtered_condition: dict) -> bool:
    for filter_key, filter_value in filtered_condition.items():
        if json_obj.get(filter_key) != filter_value:
            return False
    return True


def load_list_data(file_name: str, cls, ignore_fields=[], filtered_condition: dict = {}) -> list:
    file_path = f'{get_data_folder()}/{file_name}'
    json_list = load_json_list(file_path)
    result = []
    for json_obj in json_list:
        if not filter_obj(json_obj, filtered_condition):
            continue
        for field in ignore_fields:
            json_obj.pop(field)
        result.append(cls.from_dict(json_obj))

    return result


def delete_data(file_name: str, id_value: str, id_field: str):
    file_path = f'{get_data_folder()}/{file_name}'
    json_list = load_json_list(file_path)
    store_list = []
    for json_obj in json_list:
        if json_obj.get(id_field) != id_value:
            store_list.append(json_list)
    json_object = json.dumps(store_list, indent=4)
    with open(file_path, "w") as outfile:
        outfile.write(json_object)


def update_data(file_name: str, id_value: str, id_field: str, new_obj):
    file_path = f'{get_data_folder()}/{file_name}'
    json_list = load_json_list(file_path)
    store_list = []
    for json_obj in json_list:
        if json_obj.get(id_field) == id_value:
            store_list.append(deepcopy(new_obj.__dict__))
        else:
            store_list.append(json_obj)
    json_object = json.dumps(store_list, indent=4)
    with open(file_path, "w") as outfile:
        outfile.write(json_object)

def store_data(file_name: str, obj: Any, all_fields: List[str] = None):
    file_path = f'{get_data_folder()}/{file_name}'
    json_data = deepcopy(obj.__dict__)
    if all_fields:
        for field in json_data:
            if field not in all_fields:
                json_data.pop(field)
    json_list = load_json_list(file_path)
    json_list.append(json_data)
    json_object = json.dumps(json_list, indent=4)

    # Writing to sample.json
    with open(file_path, "w") as outfile:
        outfile.write(json_object)
