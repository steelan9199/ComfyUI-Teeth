import torch
import codecs
import numpy as np


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_typ = AnyType("*")


class indexList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_list": (any_typ, {}),
                "index": (
                    "INT",
                    {"default": 0, "min": -999999, "max": 999999, "step": 1},
                ),
            }
        }

    RETURN_TYPES = (any_typ,)
    RETURN_NAMES = ("element",)
    INPUT_IS_LIST = True
    FUNCTION = "get_element"
    CATEGORY = "Teeth"

    def get_element(self, input_list, index):
        index = index[0]
        if isinstance(input_list, (list, tuple)):
            elements = input_list
            are_all_tensors = all(
                isinstance(element, torch.Tensor) for element in elements
            )
            if are_all_tensors:
                element = input_list[index]
                return (element,)
            else:
                print("[indexList] input_list is not all tensors.")
                elements = elements[0]
                return (elements[index],)
        else:
            print("[indexList] input_list is not a list or tuple.")
            raise TypeError(f"Input must be a list or tuple, got {type(input_list)}")


class TextSplitByDelimiter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "delimiter": (
                    "STRING",
                    {"multiline": False, "default": ",", "dynamicPrompts": False},
                ),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("list",)

    FUNCTION = "run"
    CATEGORY = "Teeth"

    def run(self, text, delimiter):
        if delimiter == "":
            arr = [text.strip()]
        else:
            delimiter = codecs.decode(delimiter, "unicode_escape")
            arr = [line for line in text.split(delimiter) if line.strip()]
        return (arr,)
