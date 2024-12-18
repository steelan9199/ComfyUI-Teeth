from PIL import Image
import numpy as np
import torch
import os
import datetime


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_typ = AnyType("*")


class SplitGridImage:
    """
    一个用于将四宫格或九宫格图片拆分为单独图片的 ComfyUI 自定义节点。
    返回一个包含拆分后图片的 Tensor 的列表，并自动保存图片到指定文件夹。
    """

    def __init__(self):
        self.output_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "output",
        )

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "grid_type": (["4", "9"], {"default": "4"}),
                "folder_path": ("STRING", {"default": "output"}),
            },
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("image_list",)
    FUNCTION = "split_image"
    CATEGORY = "Teeth"
    OUTPUT_NODE = True

    def split_image(self, image, grid_type, folder_path):
        """
        将四宫格或九宫格图片拆分为多张图片，保存到指定文件夹, 并返回一个包含这些图片的列表。

        Args:
            image: 输入的四宫格或九宫格图片 (Tensor)。
            grid_type: 宫格类型，"4" 表示四宫格，"9" 表示九宫格。
            folder_path: 保存图片的文件夹路径。

        Returns:
            一个包含拆分后图片 Tensor 的列表。
        """
        # 将 Tensor 转换为 NumPy 数组
        i = 255.0 * image.cpu().numpy().squeeze()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        # 获取图片的宽度和高度
        width, height = img.size

        # 根据宫格类型计算子图数量和行列数
        if grid_type == "4":
            num_cols = 2
            num_rows = 2
        elif grid_type == "9":
            num_cols = 3
            num_rows = 3
        else:
            raise ValueError(f"Invalid grid_type: {grid_type}")

        # 计算每个子图的宽度和高度
        sub_width = width // num_cols
        sub_height = height // num_rows

        # 分割图片并创建子图
        images = []

        sub_images = {}  # 使用字典临时存储子图及其索引

        for i in range(num_rows):
            for j in range(num_cols):
                left = j * sub_width
                upper = i * sub_height
                right = (j + 1) * sub_width
                lower = (i + 1) * sub_height

                sub_image = img.crop((left, upper, right, lower))
                # 构建文件名和完整保存路径
                index = i * num_cols + j  # 使用从0开始的索引

                sub_images[index] = sub_image

        for index in range(len(sub_images)):
            # 获取当前时间，包含毫秒
            now = datetime.datetime.now()
            current_time = now.strftime("%H%M%S%f")[:-3]  # 时分秒毫秒 (最后三位是毫秒)

            # 构建文件名和完整保存路径, 这里编号改成从1开始
            file_name = f"{index+1}-{current_time}.png"

            #  如果用户没有指定文件夹路径，则使用默认的输出文件夹
            if folder_path == "output":
                save_path = os.path.join(self.output_dir, file_name)
            else:
                save_path = os.path.join(folder_path, file_name)

            # 保存图片
            sub_images[index].save(save_path)
            print(f"Image saved to: {save_path}")

            # 将子图转换回 Tensor 并添加到列表中
            img_np = np.array(sub_images[index]).astype(np.float32) / 255.0
            img_tensor = torch.from_numpy(img_np)[None,]
            images.append(img_tensor)

        return (images,)
