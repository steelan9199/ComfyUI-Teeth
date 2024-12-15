from .image_selector_node import indexList, TextSplitByDelimiter
from .get_first_seg import GetFirstSeg
from .findContours import FindContours

NODE_CLASS_MAPPINGS = {
    "teeth GetValueByIndexFromList": indexList,
    "teeth TextSplitByDelimiter": TextSplitByDelimiter,
    "teeth GetFirstSeg": GetFirstSeg,
    "teeth FindContours": FindContours,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "teeth GetValueByIndexFromList": "TeethGetValueByIndexFromList",
    "teeth TextSplitByDelimiter": "TeethTextSplitByDelimiter",
    "teeth GetFirstSeg": "TeethGetFirstSeg",
    "teeth FindContours": "TeethFindContours",
}

WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
