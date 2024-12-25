import os
import time
import uuid
import folder_paths
import hashlib


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


class LoadTextFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": ""}),
                "encoding": (
                    ["utf-8", "gbk", "latin-1", "ascii"],
                    {"default": "utf-8"},
                ),
                "always_run": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "read_file"
    CATEGORY = "Teeth"

    @classmethod
    def IS_CHANGED(
        cls,
        folder,
        filename,
        encoding,
        always_run,
        **kwargs,
    ):
        if always_run:
            return float("NaN")

        input_data = f"{folder}{filename}{encoding}".encode("utf-8")
        return hashlib.sha256(input_data).hexdigest()

    def read_file(self, folder, filename, encoding, always_run):
        file_path = os.path.join(folder, filename)

        if not os.path.exists(file_path):
            log(f"Error: File not found: {file_path}", message_type="error")
            raise FileNotFoundError(f"File not found: {file_path}")

        if not os.path.isfile(file_path):
            log(f"Error: Path is not a file: {file_path}", message_type="error")
            raise ValueError(f"Path is not a file: {file_path}")

        try:
            with open(file_path, "r", encoding=encoding) as f:
                text = f.read()
            log(f"Successfully read file: {file_path}", message_type="finish")
            return (text,)
        except UnicodeDecodeError as e:
            log(
                f"Error: Failed to decode file with encoding '{encoding}'. Try a different encoding. Error: {e}",
                message_type="error",
            )
            raise
        except Exception as e:
            log(
                f"Error: An unexpected error occurred while reading the file: {e}",
                message_type="error",
            )
            raise


class SaveTextFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": (
                    "STRING",
                    {"default": "", "multiline": False, "forceInput": True},
                ),
                "folder": ("STRING", {"default": "output"}),
                "filename": ("STRING", {"default": "saved_text.txt"}),
                "add_timestamp": ("BOOLEAN", {"default": True}),
                "add_random": ("BOOLEAN", {"default": True}),
                "encoding": (
                    ["utf-8", "gbk", "latin-1", "ascii"],
                    {"default": "utf-8"},
                ),
                "always_run": ("BOOLEAN", {"default": False}),
            }
        }

    @classmethod
    def IS_CHANGED(
        cls,
        text,
        folder,
        filename,
        add_timestamp,
        add_random,
        encoding,
        always_run,
        **kwargs,
    ):
        if always_run:
            return float("NaN")
        # 注意这里, 我们将always_run也加入hash
        input_data = f"{text}{folder}{filename}{add_timestamp}{add_random}{encoding}{always_run}".encode(
            "utf-8"
        )
        return hashlib.sha256(input_data).hexdigest()

    RETURN_TYPES = ()
    FUNCTION = "write_file"
    CATEGORY = "Teeth"
    OUTPUT_NODE = True

    def write_file(
        self, text, folder, filename, add_timestamp, add_random, encoding, always_run
    ):
        # 检查文件夹路径是否为空
        if not folder:
            log("Error: Folder path is required.", message_type="error")
            raise ValueError("Folder path is required.")
        if folder == "output":
            output_dir = folder_paths.get_output_directory()
            folder = output_dir

        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                log(f"Created folder: {folder}")
            except Exception as e:
                log(
                    f"Error: Failed to create folder: {folder}. Error: {e}",
                    message_type="error",
                )
                raise
        # 提取文件名和后缀
        name_without_ext, ext = os.path.splitext(filename)
        timestamp = ""
        if add_timestamp:
            timestamp = time.strftime("%Y%m%d_%H%M%S")

        random_str = ""
        if add_random:
            random_str = "_" + str(uuid.uuid4())[:8]
        # 重新组合文件名
        new_filename = f"{name_without_ext}{timestamp}{random_str}{ext}"
        file_path = os.path.join(folder, new_filename)
        try:
            with open(file_path, "w", encoding=encoding) as f:
                f.write(text)
            log(f"Successfully saved file: {file_path}", message_type="finish")
            return ()
        except Exception as e:
            log(
                f"Error: Failed to write to file: {file_path}. Error: {e}",
                message_type="error",
            )
            raise
