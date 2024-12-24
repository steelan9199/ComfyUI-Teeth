import folder_paths
from PIL import Image
import torch
from google import genai
from google.genai import types
import os
import numpy as np
import io


def log(message: str, message_type: str = "info"):
    name = "Teeth"

    if message_type == "error":
        message = "\033[1;41m" + message + "\033[m"
    elif message_type == "warning":
        message = "\033[1;31m" + message + "\033[m"
    elif message_type == "finish":
        message = "\033[1;32m" + message + "\033[m"
    else:
        message = "\033[1;33m" + message + "\033[m"
    print(f"{name} -> {message}")


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_typ = AnyType("*")


class Gemini2:
    def tensor_to_pil(self, tensor):
        # 将 ComfyUI 的图像 tensor 转换为 PIL Image 对象
        i = 255.0 * tensor.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        return img

    def get_api_key(api_name: str) -> str:
        api_key_ini_file = os.path.join(
            os.path.dirname(os.path.normpath(__file__)), "api_key.ini"
        )
        ret_value = ""
        try:
            with open(api_key_ini_file, "r") as f:
                ini = f.readlines()
                for line in ini:
                    line = line.strip()
                    parts = line.split("=")
                    if len(parts) == 2 and parts[0].strip() == api_name:
                        ret_value = parts[1].strip()
                        break
        except Exception as e:
            log(
                f"Warning: {api_key_ini_file} "
                + repr(e)
                + ", check it to be correct. ",
                message_type="warning",
            )
        remove_char = ['"', "'", "“", "”", "‘", "’"]
        for i in remove_char:
            if i in ret_value:
                ret_value = ret_value.replace(i, "")
        if len(ret_value) < 4:
            log(
                f"Warning: Invalid API-key, Check the key in {api_key_ini_file}.",
                message_type="warning",
            )
        if ret_value:
            return ret_value
        else:
            raise ValueError(
                f'API key not found in "{api_key_ini_file}". Please ensure the file exists and contains: google_api_key = YOUR_API_KEY\n'
                f"You can apply for an API key here: https://aistudio.google.com/app/apikey"
            )

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        print("input_dir", input_dir)
        return {
            "required": {
                "model": (
                    [
                        "gemini-1.5-flash(15RPM,平衡)",
                        "gemini-2.0-flash-exp(10RPM,最新)",
                        "gemini-1.5-pro(2RPM,最佳)",
                        "gemini-1.5-flash-8b(15RPM,低能)",
                    ],
                ),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                    },
                ),
            },
            "optional": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                    },
                ),
                "prompt2": (any_typ,),
                "prompt3": (any_typ,),
                "prompt4": (any_typ,),
                "prompt5": (any_typ,),
                "prompt6": (any_typ,),
                "prompt7": (any_typ,),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "doit"
    CATEGORY = "Teeth"

    def doit(self, model, prompt, **kwargs):
        api_key = self.get_api_key("google_api_key")
        inputItems = []
        if prompt:
            inputItems.append(prompt)
        # 遍历所有可选输入
        for input_name, data in kwargs.items():
            if data is None:
                continue

            if isinstance(data, str):
                # 文本
                inputItems.append(data)
            elif isinstance(data, torch.Tensor):
                # 图像
                pil_image = self.tensor_to_pil(data)

                # 生成一个唯一的文件名，例如使用时间戳
                import time

                timestamp = int(time.time() * 1000)
                temp_folder = r"D:\temp"
                filename = os.path.join(temp_folder, f"image_{timestamp}.jpg")
                pil_image.save(filename, format="JPEG")
                log(f"Image saved to: {filename}")  # 打印保存路径

                # 使用 BytesIO 将 PIL 图像保存到内存中的字节流
                byte_stream = io.BytesIO()
                pil_image.save(byte_stream, format="JPEG")
                image_bytes = byte_stream.getvalue()
                inputItems.append(
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                )
            else:
                raise ValueError(
                    f"Error: Input '{input_name}' has an unsupported type: {type(data)}. Only text (string) and images (tensor) are allowed."
                )
        # 检查inputItems的长度, 如果长度为0, 就抛出错误, 提示用户.
        if len(inputItems) == 0:
            raise ValueError(
                "Error: No input provided. Please provide at least one input."
            )
        # 发送给 Gemini
        client = genai.Client(api_key=api_key)
        model_name = model.split("(")[0]
        response = client.models.generate_content(
            model=model_name,
            contents=inputItems,
        )
        return (response.text,)
