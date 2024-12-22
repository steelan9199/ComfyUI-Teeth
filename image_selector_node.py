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
            if -len(input_list) <= index < len(input_list):
                element = input_list[index]
                if isinstance(element, torch.Tensor):
                    return (element,)  # Tensor type, return directly
                elif isinstance(element, np.ndarray):
                    return (element,)  # numpy array, return directly
                elif isinstance(element, int):
                    return (element,)  # 整数, 直接返回
                elif isinstance(element, float):
                    return (element,)  # 浮点数, 直接返回
                elif isinstance(element, str):
                    return (element,)  # 字符串, 直接返回
                else:
                    return (torch.tensor([element]),)  # Fallback: convert to tensor
            else:
                raise IndexError(
                    f"Index {index} is out of range for list of length {len(input_list)}"
                )
        elif isinstance(input_list, torch.Tensor):
            if 0 <= index < input_list.shape[0]:
                return (
                    input_list[index : index + 1].clone(),
                )  # Always return tensor slice for tensor input
            else:
                raise IndexError(
                    f"Index {index} is out of range for tensor of shape {input_list.shape}"
                )
        else:
            raise TypeError(
                f"Input must be a list, tuple, or tensor, got {type(input_list)}, value is {input_list}"
            )


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
