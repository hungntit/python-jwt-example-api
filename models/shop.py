import json
from copy import deepcopy
from typing import List, Optional
from uuid import uuid4
from utils.load_json_file import load_list_data, store_data, delete_data, update_data


class Shop:

    def __init__(self, name: str = None, address: str = None, user_id: str = None):
        self.name = name
        self.address = address
        self.user_id = user_id
        self.id = None

    def update(self, json_data):
        for key in json_data:
            if key in Shop.all_fields() and key not in Shop.not_modified_fields():
                setattr(self, key, json_data[key])
        update_data('shops.json', self.id, Shop.id_field(), self)

    def save(self):
        if not self.id:
            self.id = str(uuid4())
        store_data(f'shops.json', self, all_fields=Shop.all_fields())

    def delete(self):
        delete_data('shops.json', self.id, Shop.id_field())

    def to_safe_json(self) -> dict:
        json_data = deepcopy(self.__dict__)
        return json_data

    def json_stringify(self):
        return json.dumps(self.to_safe_json())

    @classmethod
    def from_dict(cls, datadict):
        obj = cls()
        for key in datadict:
            if key in cls.all_fields():
                setattr(obj, key, datadict[key])
        return obj

    @classmethod
    def load_data(cls, filtered_condition: dict = {}) -> list:
        ignore_fields = []
        return load_list_data('shops.json', cls, ignore_fields, filtered_condition=filtered_condition)

    @classmethod
    def find_all_by_user_id(cls, user_id) -> list:
        return cls.load_data(filtered_condition={'user_id': user_id})

    @classmethod
    def load_by_id(cls, user_id: str, shop_id: str):
        shops = cls.load_data(filtered_condition={'user_id': user_id, 'id': shop_id})
        result: Optional[Shop] = None
        if shops:
            result = shops[0]
        return result

    @classmethod
    def required_fields(cls):
        return ['name', 'address']

    @classmethod
    def data_fields(cls):
        return ['name', 'address', 'user_id']

    @classmethod
    def not_modified_fields(cls):
        return ['user_id', 'id']

    @classmethod
    def all_fields(cls) -> List[str]:
        fields = cls.data_fields()
        fields.append(cls.id_field())
        return fields

    @classmethod
    def id_field(cls):
        return "id"

    @classmethod
    def validate_error(cls, json_obj: dict, created: bool = False):
        if created:
            required_fields = cls.required_fields()
        else:
            required_fields = cls.required_fields()
        for field in required_fields:
            if field not in json_obj:
                return f"{field} is missing"
