import folder_paths
import os
import platform
import subprocess
from server import PromptServer
from aiohttp import web


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


def open_folder(folder_path):
    """
    Opens the specified folder using the operating system's default file explorer.

    Args:
        folder_path: The path to the folder to open.
    """
    if platform.system() == "Windows":
        # Use explorer.exe on Windows
        os.startfile(folder_path)
    elif platform.system() == "Darwin":
        # Use open command on macOS
        subprocess.Popen(["open", folder_path])
    elif platform.system() == "Linux":
        # Use xdg-open on Linux
        subprocess.Popen(["xdg-open", folder_path])
    else:
        raise ValueError(f"Error: Unsupported operating system: {platform.system()}")


# https://docs.comfy.org/essentials/comms_routes#routes
def register_routes():
    @PromptServer.instance.routes.post("/teeth/gemini/opendir")
    async def get_comfyui_folderInfo(request):
        data = await request.json()
        folder = data.get("folder")
        # 检查文件夹路径是否为空
        if not folder:
            log("Error: Folder path is required.", message_type="error")
            raise ValueError("Folder path is required.")
        if folder == "output":
            output_dir = folder_paths.get_output_directory()
            folder = output_dir

        # 检查文件夹是否存在, 如果不存在则抛出错误
        if not os.path.exists(folder):
            log(f"Error: Folder does not exist: {folder}", message_type="error")
            raise FileNotFoundError(f"Folder does not exist: {folder}")
        open_folder(folder)
        return web.json_response({"success": "ok"}, status=200)
