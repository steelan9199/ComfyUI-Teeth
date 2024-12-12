from .image_selector_node import indexList, TextSplitByDelimiter
from .get_first_seg import GetFirstSeg

NODE_CLASS_MAPPINGS = {
    "GetValueByIndexFromList": indexList,
    "TextSplitByDelimiter": TextSplitByDelimiter,
    "GetFirstSeg": GetFirstSeg,
}

__all__ = ["NODE_CLASS_MAPPINGS"]
