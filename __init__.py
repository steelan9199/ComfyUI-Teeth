from .image_selector_node import indexList, TextSplitByDelimiter
from .get_first_seg import GetFirstSeg
from .findContours import FindContours

NODE_CLASS_MAPPINGS = {
    "GetValueByIndexFromList": indexList,
    "TextSplitByDelimiter": TextSplitByDelimiter,
    "GetFirstSeg": GetFirstSeg,
    "FindContours": FindContours,
}

__all__ = ["NODE_CLASS_MAPPINGS"]
