import textwrap


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_typ = AnyType("*")


class RunPythonCode:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "code": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "result = value1 + value2",
                    },
                ),
            },
            "optional": {
                "value1": (any_typ,),
                "value2": (any_typ,),
                "value3": (any_typ,),
                "value4": (any_typ,),
                "value5": (any_typ,),
                "value6": (any_typ,),
            },
        }

    RETURN_TYPES = (any_typ,)
    RETURN_NAMES = ("result",)
    FUNCTION = "run_python_code"
    CATEGORY = "Teeth"

    def run_python_code(self, code, **kwargs):
        # 使用 textwrap.dedent() 移除代码中的缩进
        dedented_code = textwrap.dedent(code)
        # 从 kwargs 中获取所有输入参数，排除 code
        inputs = {key: value for key, value in kwargs.items() if key not in ["code"]}

        # 创建一个局部字典作为 exec() 的命名空间
        local_vars = inputs.copy()
        try:
            # 执行 Python 代码
            exec(dedented_code, {}, local_vars)
            # 确保 result 是一个列表
            result = local_vars.get("result", None)
            if result is None:
                print(
                    "Warning: 'result' variable not defined in user code. Returning None."
                )
                return (None,)
            else:
                return (result,)

        except Exception as e:
            # 捕获异常并打印错误信息
            print(f"Error in Python code: {e}")
            return (None,)

    # @classmethod
    # def IS_CHANGED(cls, code, **kwargs):
    #     # 强制节点每次都重新计算
    #     return float("NaN")
