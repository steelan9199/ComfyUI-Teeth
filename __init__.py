from .image_selector_node import indexList, TextSplitByDelimiter
from .get_first_seg import GetFirstSeg
from .findContours import FindContours
from .run_python_code import RunPythonCode


NODE_CLASS_MAPPINGS = {
    "teeth GetValueByIndexFromList": indexList,
    "teeth TextSplitByDelimiter": TextSplitByDelimiter,
    "teeth GetFirstSeg": GetFirstSeg,
    "teeth FindContours": FindContours,
    "teeth RunPythonCode": RunPythonCode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "teeth GetValueByIndexFromList": "TeethGetValueByIndexFromList",
    "teeth TextSplitByDelimiter": "TeethTextSplitByDelimiter",
    "teeth GetFirstSeg": "TeethGetFirstSeg",
    "teeth FindContours": "TeethFindContours",
    "teeth RunPythonCode": "TeethRunPythonCode",
}

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
