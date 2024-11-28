from .image_selector_node import indexList, TextSplitByDelimiter

NODE_CLASS_MAPPINGS = {
    "Index List": indexList,
    "TextSplitByDelimiter": TextSplitByDelimiter,
}

__all__ = ["NODE_CLASS_MAPPINGS"]
