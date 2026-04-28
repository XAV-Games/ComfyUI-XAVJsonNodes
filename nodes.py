import json
import os
from uuid import uuid4

FILE_CACHE = {}
OBJ_CACHE = {}


class LoadJSONFile:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_ref",)
    FUNCTION = "load_json"
    CATEGORY = "XAV/json"

    def load_json(self, file_path):
        if file_path in FILE_CACHE:
            root_obj = FILE_CACHE[file_path]
        else:
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"JSON file not found: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                root_obj = json.load(f)
            FILE_CACHE[file_path] = root_obj

        ref_id = str(uuid4())
        OBJ_CACHE[ref_id] = root_obj
        return (ref_id,)


class NavigateJSON:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_ref": ("STRING", {"forceInput": True}),
                "key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_ref",)
    FUNCTION = "navigate"
    CATEGORY = "XAV/json"

    def navigate(self, json_ref, key):
        obj = OBJ_CACHE.get(json_ref)
        if obj is None:
            sub_obj = None
        elif isinstance(obj, list):
            try:
                idx = int(key)
                sub_obj = obj[idx] if 0 <= idx < len(obj) else None
            except (ValueError, IndexError):
                sub_obj = None
        elif isinstance(obj, dict):
            sub_obj = obj.get(key, None)
        else:
            sub_obj = None

        new_ref = str(uuid4())
        OBJ_CACHE[new_ref] = sub_obj
        return (new_ref,)


class JSONToPrimitives:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_ref": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "BOOLEAN", "STRING")
    RETURN_NAMES = ("int_val", "float_val", "bool_val", "str_val")
    FUNCTION = "convert"
    CATEGORY = "XAV/json"

    def convert(self, json_ref):
        obj = OBJ_CACHE.get(json_ref)

        try:
            int_val = int(obj)
        except (ValueError, TypeError):
            int_val = 0

        try:
            float_val = float(obj)
        except (ValueError, TypeError):
            float_val = 0.0

        if obj is None:
            bool_val = False
        elif isinstance(obj, bool):
            bool_val = obj
        elif isinstance(obj, str):
            bool_val = obj.strip().lower() in ("true", "1", "yes")
        else:
            bool_val = bool(obj)

        if obj is None:
            str_val = ""
        else:
            str_val = str(obj)

        return (int_val, float_val, bool_val, str_val)


class CreateEmptyJSONObject:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "is_array": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_ref",)
    FUNCTION = "create"
    CATEGORY = "XAV/json"

    def create(self, is_array):
        node_key = f"empty_node_{id(self)}"
        if node_key in OBJ_CACHE:
            existing_obj = OBJ_CACHE[node_key]
            if (is_array and isinstance(existing_obj, list)) or (not is_array and isinstance(existing_obj, dict)):
                return (node_key,)

        new_obj = [] if is_array else {}
        OBJ_CACHE[node_key] = new_obj
        return (node_key,)


class SetJSONValue:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_ref": ("STRING", {"forceInput": True}),
                "key": ("STRING", {"default": ""}),
                "value": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_ref",)
    FUNCTION = "set_value"
    CATEGORY = "XAV/json"

    def set_value(self, json_ref, key, value):
        obj = OBJ_CACHE.get(json_ref)
        if obj is None:
            return (json_ref,)

        if isinstance(obj, list):
            try:
                idx = int(key)
                if 0 <= idx < len(obj):
                    obj[idx] = value
            except ValueError:
                pass
        elif isinstance(obj, dict):
            obj[key] = value

        return (json_ref,)


class SetJSONValueFromRef:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_ref": ("STRING", {"forceInput": True}),
                "key": ("STRING", {"default": ""}),
                "value_ref": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_ref",)
    FUNCTION = "set_value_ref"
    CATEGORY = "XAV/json"

    def set_value_ref(self, json_ref, key, value_ref):
        obj = OBJ_CACHE.get(json_ref)
        val = OBJ_CACHE.get(value_ref)
        if obj is None:
            return (json_ref,)

        if isinstance(obj, list):
            try:
                idx = int(key)
                if 0 <= idx < len(obj):
                    obj[idx] = val
            except ValueError:
                pass
        elif isinstance(obj, dict):
            obj[key] = val

        return (json_ref,)


class SaveJSONToFile:
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_ref": ("STRING", {"forceInput": True}),
                "file_path": ("STRING", {"default": "", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_path",)
    FUNCTION = "save"
    CATEGORY = "XAV/json"

    def save(self, json_ref, file_path):
        obj = OBJ_CACHE.get(json_ref)
        if obj is None:
            obj = None

        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)

        return (file_path,)