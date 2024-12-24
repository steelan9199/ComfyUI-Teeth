from .image_selector_node import indexList, TextSplitByDelimiter
from .get_first_seg import GetFirstSeg
from .findContours import FindContours
from .run_python_code import RunPythonCode
from .splitGridImage import SplitGridImage
from .image_grid_lines import ImageGridLines
from .gemini2 import Gemini2


NODE_CLASS_MAPPINGS = {
    "teeth GetValueByIndexFromList": indexList,
    "teeth TextSplitByDelimiter": TextSplitByDelimiter,
    "teeth GetFirstSeg": GetFirstSeg,
    "teeth FindContours": FindContours,
    "teeth RunPythonCode": RunPythonCode,
    "teeth SplitGridImage": SplitGridImage,
    "teeth ImageGridLines": ImageGridLines,
    "teeth Gemini2": Gemini2,
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
}

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
