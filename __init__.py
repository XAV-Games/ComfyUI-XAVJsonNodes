NODE_ID = "comfyui-xav-json-nodes"

from .nodes import (
    LoadJSONFile,
    NavigateJSON,
    JSONToPrimitives,
    CreateEmptyJSONObject,
    SetJSONValue,
    SetJSONValueFromRef,
    SaveJSONToFile,
)

NODE_CLASS_MAPPINGS = {
    "XAVLoadJSONFile": LoadJSONFile,
    "XAVNavigateJSON": NavigateJSON,
    "XAVJSONToPrimitives": JSONToPrimitives,
    "XAVCreateEmptyJSONObject": CreateEmptyJSONObject,
    "XAVSetJSONValue": SetJSONValue,
    "XAVSetJSONValueFromRef": SetJSONValueFromRef,
    "XAVSaveJSONToFile": SaveJSONToFile,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "XAVLoadJSONFile": "XAV Load JSON File",
    "XAVNavigateJSON": "XAV Navigate JSON",
    "XAVJSONToPrimitives": "XAV JSON to Primitives",
    "XAVCreateEmptyJSONObject": "XAV Create Empty JSON Object",
    "XAVSetJSONValue": "XAV Set JSON Value",
    "XAVSetJSONValueFromRef": "XAV Set JSON Value From Ref",
    "XAVSaveJSONToFile": "XAV Save JSON to File",
}