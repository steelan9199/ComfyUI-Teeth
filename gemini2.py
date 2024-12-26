import PIL
import torch
from google import genai

# https://github.com/googleapis/python-genai
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
        tensor = tensor.cpu().squeeze()
        print("Shape after squeeze:", tensor.shape)

        if tensor.ndim == 3:
            if tensor.shape[0] == 3:
                tensor = tensor.permute(1, 2, 0)
            elif tensor.shape[2] == 3:
                pass
            else:
                raise ValueError(
                    f"Tensor shape {tensor.shape} is not supported. Expected (3, H, W) or (H, W, 3)"
                )
        else:
            raise ValueError(f"Tensor shape {tensor.shape} is not supported.")

        print("Shape before converting to PIL:", tensor.shape)
        tensor = tensor.clamp(0, 1) * 255

        img = PIL.Image.fromarray(tensor.numpy().astype(np.uint8))
        return img

    def get_api_key(self, api_name: str) -> str:
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
                "temperature": (
                    "FLOAT",
                    {
                        "default": 0.5,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "display": "slider",
                    },
                ),
                "top_p": (
                    "FLOAT",
                    {
                        "default": 0.9,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "display": "slider",
                    },
                ),
                "top_k": (
                    "INT",
                    {
                        "default": 20,
                        "min": 0,
                        "max": 100,
                        "step": 1,
                        "display": "slider",
                    },
                ),
                "max_output_tokens": (
                    "INT",
                    {
                        "default": 8192,
                        "min": 1,
                        "max": 8192,
                        "step": 1,
                    },
                ),
                "presence_penalty": (
                    "FLOAT",
                    {
                        "default": 0.3,
                        "min": -2.0,
                        "max": 2.0,
                        "step": 0.01,
                        "display": "slider",
                    },
                ),
                "frequency_penalty": (
                    "FLOAT",
                    {
                        "default": 0.3,
                        "min": -2.0,
                        "max": 2.0,
                        "step": 0.01,
                        "display": "slider",
                    },
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

    def doit(
        self,
        model,
        prompt,
        temperature,
        top_p,
        top_k,
        max_output_tokens,
        presence_penalty,
        frequency_penalty,
        **kwargs,
    ):
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
                # 使用 BytesIO 将 PIL 图像保存到内存中的字节流
                byte_stream = io.BytesIO()
                pil_image.save(byte_stream, format="JPEG")
                image_bytes = byte_stream.getvalue()
                inputItems.append(
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                )
            else:
                raise ValueError(
                    f"Error: Input '{input_name}' has an unsupported type: {type(data)}. Only text and image are allowed."
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
            config=types.GenerateContentConfig(
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                candidate_count=1,
                max_output_tokens=max_output_tokens,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
            ),
        )
        return (response.text,)


"""
        response = client.models.generate_content(
            model=model_name,
            contents=inputItems,
            config=types.GenerateContentConfig(
                temperature=0.5,
                top_p=0.9,
                top_k=20,
                candidate_count=1,
                max_output_tokens=8192,
                presence_penalty=0.3,
                frequency_penalty=0.3,
            ),
        )

参数范围和默认值：

temperature:

范围: 0.0 - 1.0

步长: 0.01

默认值: 0.5

top_p:

范围: 0.0 - 1.0

步长: 0.01

默认值: 0.9

top_k:

范围: 0 - 100

步长: 1

默认值: 20

max_output_tokens:

范围: 1 - 8192

步长: 1

默认值: 8192

presence_penalty:

范围: -2.0 - 2.0

步长: 0.01

默认值: 0.3

frequency_penalty:

范围: -2.0 - 2.0

步长: 0.01

默认值: 0.3

stop_sequences:

默认值: "" (空字符串)

好的，我查看了你提供的 Google AI Python 客户端库的官方文档：[https://googleapis.github.io/python-genai/](https://googleapis.github.io/python-genai/)

关于 `GenerateContentConfig` 中的各个参数，我来解释一下它们的含义、最佳值选择的考量以及文档中记录的默认值：

**1. `temperature` (温度):**

*   **含义:** 控制生成文本的随机性。值越高，生成的文本越随机、越有创意；值越低，生成的文本越确定、越可预测。
*   **最佳值:**
    *   对于需要精确性和确定性的任务（例如，代码生成、技术文档），建议使用较低的温度，如 `0`, `0.1`, `0.2`。
    *   对于需要创造性和多样性的任务（例如，故事创作、诗歌生成），可以使用较高的温度，如 `0.7`, `0.8`, `0.9`。
    *   对于大多数一般的文本生成任务，`0.3` 到 `0.6` 之间的温度通常效果不错。
*   **默认值:** 文档中没有明确说明 `temperature` 的默认值，但根据 Google AI 的其他文档和惯例，推测默认值可能在 `0.7` 或 `0.9` 左右。 

**2. `top_p` (核心采样):**

*   **含义:**  控制模型在生成文本时考虑的候选词的范围。值越小，模型考虑的候选词越少，生成的结果越确定；值越大，模型考虑的候选词越多，生成的结果越多样。`top_p` 是一个累积概率阈值。例如，`top_p=0.9` 表示模型会考虑累积概率达到 90% 的候选词。
*   **最佳值:**  `top_p` 通常与 `temperature` 结合使用。当 `temperature` 较高时，可以适当降低 `top_p` 以限制过于离散的生成结果。一般来说：
    *   对于需要精确性和确定性的任务，建议使用较低的 `top_p`，如 `0.5`, `0.7`。
    *   对于需要创造性和多样性的任务，可以使用较高的 `top_p`，如 `0.9`, `0.95`。
*   **默认值:** 文档中没有明确说明 `top_p` 的默认值，根据经验和常见的做法，推测默认值可能在 `0.9` 或 `1.0` 左右。

**3. `top_k` (Top-K 采样):**

*   **含义:**  控制模型在生成文本时考虑的候选词的数量。值越小，模型考虑的候选词越少，生成的结果越确定；值越大，模型考虑的候选词越多，生成的结果越多样。`top_k` 是一个绝对数量阈值。例如，`top_k=40` 表示模型在每个生成步骤中只考虑概率最高的 40 个候选词。
*   **最佳值:** `top_k` 通常也与 `temperature` 结合使用。
    *   对于需要精确性和确定性的任务，可以使用较小的 `top_k`，如 `10`, `20`。
    *   对于需要创造性和多样性的任务，可以使用较大的 `top_k`，如 `40`, `60`。
*   **默认值:** 文档中没有明确说明 `top_k` 的默认值。根据经验和常见的做法，推测默认值可能在 `40` 左右。

**4. `candidate_count` (候选计数):**

*   **含义:** 控制模型生成的候选回复的数量。
*   **最佳值:** 通常情况下，设置为 `1` 即可，表示只生成一个最佳回复。如果需要比较不同的生成结果，可以将其设置为更高的值。
*   **默认值:**  **`1`** (文档中有明确说明)

**5. `seed` (随机种子):**

*   **含义:** 用于控制随机数生成器的初始状态。设置相同的种子可以确保每次生成的结果相同，这对于调试和复现结果非常有用。
*   **最佳值:**  如果你希望每次运行代码时获得不同的生成结果，可以不设置 `seed`，或者将其设置为一个随机值。如果你希望复现某个特定的生成结果，可以将其设置为一个固定的值。
*   **默认值:** 文档中没有明确说明 `seed` 的默认值。如果没有设置，则每次运行代码时会使用不同的随机种子。

**6. `max_output_tokens` (最大输出令牌数):**

*   **含义:** 控制生成文本的最大长度（以 token 为单位）。
*   **最佳值:** 根据你的需求进行设置。对于较短的文本，可以设置为几百；对于较长的文本，可以设置为几千。需要注意，设置过大的值可能会导致生成时间过长或超出模型的限制。
*   **默认值:** 文档中没有明确说明 `max_output_tokens` 的默认值，但是他有限制, `gemini-pro-vision`模型最大支持12288 个输入`token`，4096个输出`token`。

**7. `stop_sequences` (停止序列):**

*   **含义:**  指定一个或多个字符串，当模型生成这些字符串时，将停止生成。
*   **最佳值:** 根据你的需求进行设置。例如，如果你希望模型在生成句号时停止，可以将其设置为 `["."]`。可以设置多个停止序列。
*   **默认值:**  **`[]`** (空列表，文档中有明确说明，表示不使用停止序列)

**8. `presence_penalty` (存在惩罚):**

*   **含义:** 对已生成的 token 进行惩罚，以降低重复生成相同内容的可能性。值越大，惩罚力度越大，生成的结果越不容易重复。取值范围为 -2.0 到 2.0。正值会根据到目前为止是否出现在文本中来惩罚新令牌，从而增加模型谈论新主题的可能性。
*   **最佳值:**
    *   对于需要避免重复的任务，可以使用较大的正值, 如 `0.5`, `1.0`。
    *   如果允许重复或者希望生成的内容更集中，可以使用较小的值或 `0.0`。
*   **默认值:** 文档中没有明确说明 `presence_penalty` 的默认值，根据经验和常见的做法，推测默认值可能为 `0.0` 或接近 `0.0`。

**9. `frequency_penalty` (频率惩罚):**

*   **含义:** 对高频 token 进行惩罚，以降低生成常见词汇的可能性。值越大，惩罚力度越大，生成的结果越倾向于使用不常见的词汇。取值范围为 -2.0 到 2.0。正值会根据新令牌在文本中的现有频率对其进行比例惩罚，从而降低模型重复相同语句的可能性。
*   **最佳值:**
    *   对于需要生成多样化文本的任务，可以使用较大的正值，如 `0.5`, `1.0`。
    *   如果希望生成的内容更自然流畅，可以使用较小的值或 `0.0`。
*   **默认值:** 文档中没有明确说明 `frequency_penalty` 的默认值，根据经验和常见的做法，推测默认值可能为 `0.0` 或接近 `0.0`。
"""
