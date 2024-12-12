from collections import namedtuple


class GetFirstSeg:

    SEG = namedtuple(
        "SEG",
        [
            "cropped_image",
            "cropped_mask",
            "confidence",
            "crop_region",
            "bbox",
            "label",
            "control_net_wrapper",
        ],
        defaults=[None],
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "segs": ("SEGS", {}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT", "INT", "INT", "INT", "INT")
    RETURN_NAMES = (
        "CenterX",
        "CenterY",
        "Left",
        "Top",
        "Right",
        "Bottom",
        "Width",
        "Height",
    )

    FUNCTION = "getFirstSeg"
    CATEGORY = "Teeth"

    def getFirstSeg(self, segs):
        # 只处理segs列表中的第一个SEG对象
        if (
            not segs
            or len(segs) < 2
            or not segs[1]
            or not isinstance(segs[1], list)
            or not segs[1]
        ):
            raise ValueError("Invalid segs structure or no SEG object provided")

        seg = segs[1][0]  # 获取segs列表中的第一个SEG对象

        if seg is None or seg.bbox is None:
            raise ValueError("No SEG object or bbox is provided")

        # 解包bbox的值
        x1, y1, x2, y2 = seg.bbox

        # 计算中心点坐标
        centerX = (x1 + x2) // 2
        centerY = (y1 + y2) // 2

        # bbox的左上角和右下角坐标
        left = x1
        top = y1
        right = x2
        bottom = y2

        # 计算宽度和高度
        width = x2 - x1
        height = y2 - y1

        return (centerX, centerY, left, top, right, bottom, width, height)
