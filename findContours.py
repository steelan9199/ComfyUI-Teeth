import cv2
import torch
import numpy as np


class FindContours:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "threshold_thresh": (
                    "INT",
                    {
                        "default": 180,
                        "min": 0,
                        "max": 255,
                        "step": 1,
                        "display": "slider",
                    },
                ),
                "min_width": (
                    "INT",
                    {"default": 1, "min": 0, "max": 1000000, "step": 1},
                ),
                "min_height": (
                    "INT",
                    {"default": 1, "min": 0, "max": 1000000, "step": 1},
                ),
                "max_width": (
                    "INT",
                    {"default": 33, "min": 0, "max": 1000000, "step": 1},
                ),
                "max_height": (
                    "INT",
                    {"default": 33, "min": 0, "max": 1000000, "step": 1},
                ),
                "detect_white_contours": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "label_on": "White",
                        "label_off": "Black",
                    },
                ),
            },
            "optional": {},
        }

    RETURN_TYPES = ("LIST", "MASK", "MASK", "MASK", "IMAGE", "INT")
    RETURN_NAMES = (
        "Contour_List",
        "ContoursMask",
        "GrayMask",
        "BinaryMask",
        "markedImage",
        "numContoursFound",
    )
    OUTPUT_NODE = True
    FUNCTION = "findContours"
    CATEGORY = "Teeth"

    def findContours(
        self,
        image,
        threshold_thresh,
        min_width,
        min_height,
        max_width,
        max_height,
        detect_white_contours,
    ):
        image = (image * 255).to(torch.uint8)
        image = image.squeeze(0).numpy()
        # 转换为单通道灰度图，因为轮廓检测通常在灰度图上进行
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # 二值化处理
        _, binary_image = cv2.threshold(
            gray_image, threshold_thresh, 255, cv2.THRESH_BINARY
        )

        # 根据轮廓颜色参数调整二值化处理
        if detect_white_contours:
            _, binary_image = cv2.threshold(
                gray_image, threshold_thresh, 255, cv2.THRESH_BINARY
            )
        else:
            _, binary_image = cv2.threshold(
                gray_image, threshold_thresh, 255, cv2.THRESH_BINARY_INV
            )

        # 提取轮廓
        contours, _ = cv2.findContours(
            binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        # 打印contours数量
        print(f"total Found {len(contours)} contours.")
        # 初始化轮廓信息列表
        contours_list = []
        # 创建一个普通的mask用来显示轮廓
        contoursMask = np.zeros_like(gray_image, dtype=np.uint8)  # 创建一个全0的mask
        gray_image_rgb = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        colors = [
            (0, 255, 0),  # 绿色
            (255, 0, 0),  # 蓝色
            (0, 0, 255),  # 红色
            (255, 255, 0),  # 黄色
            (255, 0, 255),  # 品红色
            (0, 255, 255),  # 青色
        ]
        for i, contour in enumerate(contours):
            # 计算轮廓的面积
            area = cv2.contourArea(contour)

            # 计算最小外接矩形
            # 包含最小外接矩形信息的元组。这个元组包含三个元素：(中心点坐标, (宽度, 高度), 旋转角度)。
            min_rect = cv2.minAreaRect(contour)

            # 获取最小外接矩形的中心点坐标、宽度、高度和旋转角度
            (center_x, center_y), (min_rect_width, min_rect_height), min_rect_angle = (
                min_rect
            )

            min_box = cv2.boxPoints(min_rect)
            min_box = np.int0(min_box)  # 将坐标转换为整数

            # 计算外接矩形
            bounding_rect = cv2.boundingRect(contour)
            bounding_x, bounding_y, bounding_w, bounding_h = bounding_rect

            # 检查轮廓是否满足所有过滤条件
            if (
                min_width <= min_rect_width <= max_width
                and min_height <= min_rect_height <= max_height
            ):
                # 将轮廓信息添加到列表中
                contours_list.append(
                    {
                        "area": area,
                        "bounding_rect_x": bounding_x,  # 外接矩形的x坐标
                        "bounding_rect_y": bounding_y,  # 外接矩形的y坐标
                        "bounding_rect_width": bounding_w,  # 外接矩形的宽度
                        "bounding_rect_height": bounding_h,  # 外接矩形的高度
                        "min_rect_coords": min_box.flatten().tolist(),  # 最小外接矩形的四个坐标
                        "min_rect_width": min_rect_width,  # 最小外接矩形的宽度
                        "min_rect_height": min_rect_height,  # 最小外接矩形的高度
                        "min_rect_angle": min_rect_angle,
                        "min_rect_center": (int(center_x), int(center_y)),
                    }
                )
                color = colors[i % len(colors)]  # 循环使用颜色
                cv2.drawContours(gray_image_rgb, [contour], -1, color, 3)
                cv2.drawContours(contoursMask, [contour], -1, 255, -1)
        contoured_image_rgb = torch.from_numpy(gray_image_rgb).unsqueeze(0) / 255.0

        # 返回mask和轮廓信息列表
        print(f"filter {len(contours_list)} contours.")

        # 将mask转换为[B, H, W]格式，符合ComfyUI的MASK格式
        contoursMask = torch.from_numpy(contoursMask).unsqueeze(0) / 255.0
        gray_image = torch.from_numpy(gray_image).unsqueeze(0) / 255.0
        binaryImage = torch.from_numpy(binary_image).unsqueeze(0) / 255.0
        result = (
            contours_list,
            contoursMask,
            gray_image,
            binaryImage,
            contoured_image_rgb,
            len(contours_list),
        )
        return {
            "ui": {"text": f"total Found {len(contours_list)} contours."},
            "result": result,
        }
