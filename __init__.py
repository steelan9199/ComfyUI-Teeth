from .image_selector_node import indexList, TextSplitByDelimiter
from .get_first_seg import GetFirstSeg
from .findContours import FindContours
from .run_python_code import RunPythonCode
from .splitGridImage import SplitGridImage
from .image_grid_lines import ImageGridLines
from .gemini2 import Gemini2
from .load_text_file import LoadTextFile, SaveTextFile
import os
from .local_api import register_routes

NODE_CLASS_MAPPINGS = {
    "teeth GetValueByIndexFromList": indexList,
    "teeth TextSplitByDelimiter": TextSplitByDelimiter,
    "teeth GetFirstSeg": GetFirstSeg,
    "teeth FindContours": FindContours,
    "teeth RunPythonCode": RunPythonCode,
    "teeth SplitGridImage": SplitGridImage,
    "teeth ImageGridLines": ImageGridLines,
    "teeth Gemini2": Gemini2,
    "teeth LoadTextFile": LoadTextFile,
    "teeth SaveTextFile": SaveTextFile,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "teeth GetValueByIndexFromList": "Teeth Get Value By Index From List",
    "teeth TextSplitByDelimiter": "Teeth Text Split By Delimiter",
    "teeth GetFirstSeg": "Teeth Get First Seg",
    "teeth FindContours": "Teeth Find Contours",
    "teeth RunPythonCode": "Teeth Run Python Code",
    "teeth SplitGridImage": "Teeth Split Grid Image",
    "teeth ImageGridLines": "Teeth Image Grid Lines",
    "teeth Gemini2": "Teeth Gemini2",
    "teeth LoadTextFile": "Teeth Load Text File",
    "teeth SaveTextFile": "Teeth Save Text File",
}

WEB_DIRECTORY = "./web"
from server import PromptServer

if hasattr(PromptServer, "instance"):
    PromptServer.instance.routes.static(
        "/teeth/web/css",
        os.path.join(os.path.dirname(__file__), "web/css"),
        follow_symlinks=True,
    )


register_routes()


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
