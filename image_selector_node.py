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
        print("input_list type:", type(input_list))
        index = index[0]
        if isinstance(input_list, (list, tuple)):
            elements = input_list
            # 打印elements类型
            are_all_tensors = all(
                isinstance(element, torch.Tensor) for element in elements
            )
            if are_all_tensors:
                element = input_list[index]
                return (element,)
            else:
                print("[indexList] input_list is not all tensors.")
                # 检查是否都是基本类型 (int, float, bool, str)
                are_all_basic_types = all(
                    isinstance(element, (int, float, bool, str)) for element in elements
                )

                if are_all_basic_types:
                    # 如果都是基本类型，直接索引
                    return (elements[index],)
                else:
                    # 包含非基本类型
                    print("[indexList] input_list contains non-basic types.")

                    # 尝试将元素转换为列表
                    try:
                        # 假设是嵌套列表或元组，取第一个元素
                        elements = elements[0]

                        # 再次检查是否都是基本类型
                        are_all_basic_types_after = all(
                            isinstance(element, (int, float, bool, str))
                            for element in elements
                        )

                        if are_all_basic_types_after:
                            return (elements[index],)
                        else:
                            print(
                                "[indexList] Nested elements are not all basic types after extraction."
                            )
                            # 在这里添加针对非基本类型元素的处理逻辑
                            # 例如，你可以尝试递归调用 get_element 函数
                            # 或者根据具体情况进行特殊处理

                            # 示例：如果元素是嵌套列表，尝试递归
                            if all(
                                isinstance(element, (list, tuple))
                                for element in elements
                            ):
                                return (self.get_element(elements, (index,)),)

                            else:
                                # 无法处理，抛出异常
                                raise TypeError("Cannot handle elements of this type.")

                    except Exception as e:
                        print(f"[indexList] Error handling non-basic types: {e}")
                        raise TypeError(f"Error handling non-basic types: {e}")
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
