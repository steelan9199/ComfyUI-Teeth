import torch
import codecs


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_typ = AnyType("*")


class indexList:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_list": ("LIST", {}),
                "index": ("INT", {"default": 0, "min": 0, "max": 1000000, "step": 1}),
            }
        }

    RETURN_TYPES = (any_typ,)
    RETURN_NAMES = ("element",)

    FUNCTION = "getIndex"
    CATEGORY = "Teeth"

    def getIndex(self, input_list, index):
        if isinstance(input_list, (list, tuple)):
            if 0 <= index < len(input_list):
                return (input_list[index],)
            else:
                raise IndexError(
                    f"Index {index} is out of range for list of length {len(input_list)}"
                )
        elif isinstance(input_list, torch.Tensor):
            if 0 <= index < input_list.shape[0]:
                return (input_list[index : index + 1].clone(),)
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
