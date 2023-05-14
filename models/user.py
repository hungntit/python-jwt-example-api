import json
import bcrypt
from uuid import uuid4
from copy import deepcopy
from typing import List, Optional
from utils.load_json_file import load_list_data, load_json_list, store_data, delete_data


class User:
    def __init__(self, username: str = None, password: str = None, fullname: str = None, birthday: str = None):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.birthday = birthday
        self.roles = []
        self.id = None

    def save(self):
        if not self.id:
            self.id = str(uuid4())
        store_data('users.json', self, all_fields=User.all_fields())

    def update(self, json_data):
        for key in json_data:
            if key in User.all_fields() and key not in User.not_modified_fields():
                setattr(self, key, json_data[key])
        self.save()

    def delete(self):
        delete_data('users.json', self.id, User.id_field())

    def encrypt_password(self):
        # generating the salt
        salt = bcrypt.gensalt()
        # Hashing the password
        hash_pwd = bcrypt.hashpw(self.password.encode('utf-8'), salt)
        self.password = hash_pwd.decode()

    def to_safe_json(self) -> dict:
        json_data = deepcopy(self.__dict__)
        json_data.pop("password")
        return json_data

    def json_stringify(self):
        return json.dumps(self.to_safe_json())

    @classmethod
    def from_dict(cls, datadict, encrypt_password: bool = False, update_role: bool = False):
        obj = cls()
        all_fields = cls.all_fields()
        if not update_role:
            all_fields.remove("roles")
        for key in datadict:
            if key in all_fields:
                setattr(obj, key, datadict[key])
        if encrypt_password:
            obj.encrypt_password()
        return obj

    @classmethod
    def load_data(cls, load_password: bool = False, filtered_condition: dict = {}) -> list:
        ignore_fields = []
        if not load_password:
            ignore_fields.append("password")
        return load_list_data('users.json', cls, ignore_fields, filtered_condition)

    @classmethod
    def auth(cls, username: str, password: str):
        if not username or not password:
            return None
        user: User = cls.load_by_username(username, load_password=True)
        if user:
            hash_pwd = user.password.encode()
            actual_pwd_encode = password.encode('utf-8')
            if bcrypt.checkpw(actual_pwd_encode, hash_pwd):
                return user
        return None

    @classmethod
    def load_by_username(cls, username: str, load_password: bool = False):
        users = cls.load_data(load_password, filtered_condition={'username': username})
        if users:
            return users[0]
        return None

    @classmethod
    def load_by_id(cls, user_id: str, load_password: bool = False):
        users = cls.load_data(load_password, filtered_condition={'id': user_id})
        if users:
            return users[0]
        return None

    @classmethod
    def not_modified_fields(cls):
        return [cls.id_field()]

    @classmethod
    def required_fields(cls):
        return ['username', 'password', 'fullname', 'birthday']

    @classmethod
    def all_fields(cls) -> List[str]:
        fields = cls.data_fields()
        fields.append(cls.id_field())
        return fields

    @classmethod
    def data_fields(cls) -> List[str]:
        return ['username', 'password', 'fullname', 'birthday', 'roles']

    @classmethod
    def id_field(cls) -> str:
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
