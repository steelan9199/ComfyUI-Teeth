from .image_selector_node import indexList, TextSplitByDelimiter
from .get_first_seg import GetFirstSeg
from .findContours import FindContours
from .run_python_code import RunPythonCode
from .splitGridImage import SplitGridImage


NODE_CLASS_MAPPINGS = {
    "teeth GetValueByIndexFromList": indexList,
    "teeth TextSplitByDelimiter": TextSplitByDelimiter,
    "teeth GetFirstSeg": GetFirstSeg,
    "teeth FindContours": FindContours,
    "teeth RunPythonCode": RunPythonCode,
    "teeth SplitGridImage": SplitGridImage,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "teeth GetValueByIndexFromList": "Teeth Get Value By Index From List",
    "teeth TextSplitByDelimiter": "Teeth Text Split By Delimiter",
    "teeth GetFirstSeg": "Teeth Get First Seg",
    "teeth FindContours": "Teeth Find Contours",
    "teeth RunPythonCode": "Teeth Run Python Code",
    "teeth SplitGridImage": "Teeth Split Grid Image",
}

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
