import numpy as np
import torch
import re
import PIL


# Define hex_to_rgb OUTSIDE of create_cross
def hex_to_rgb(hex_color):
    """Converts a hex color string (e.g., #RRGGBB) to an RGB tuple."""
    hex_color = hex_color.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", hex_color):
        raise ValueError(
            "Invalid hex color format. Use #RRGGBB (e.g., #FF0000 for red)."
        )
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


class ImageGridLines:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "border_color": (
                    "STRING",
                    {"default": "#000000"},
                ),
                "border_width": (
                    "INT",
                    {
                        "default": 10,
                        "min": 1,
                        "max": 999999999,
                        "step": 1,
                    },
                ),
                "h_grids": (
                    "INT",
                    {
                        "default": 3,
                        "min": 1,
                        "max": 999999999,
                        "step": 1,
                    },
                ),
                "v_grids": (
                    "INT",
                    {
                        "default": 3,
                        "min": 1,
                        "max": 999999999,
                        "step": 1,
                    },
                ),
            },
            "optional": {},
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("GridLinesImage",)
    FUNCTION = "doit"
    CATEGORY = "Teeth"

    def doit(self, image, border_color, border_width, h_grids, v_grids):
        """
        Draws a grid on the input image with a user-specified color,
        number of horizontal grid lines, and number of vertical grid lines.

        Args:
            image: Input image (Tensor).
            border_color: Grid line color in #RRGGBB format (string).
            border_width: Width of the grid lines (int).
            h_grids: Number of horizontal grid lines (int).
            v_grids: Number of vertical grid lines (int).

        Returns:
            Image with grid lines (Tensor).
        """

        print("Initial image shape:", image.shape)

        def tensor_to_pil(tensor):
            tensor = tensor.cpu().squeeze()
            print("Shape after squeeze:", tensor.shape)

            if tensor.ndim == 3:
                if tensor.shape[0] == 3:
                    tensor = tensor.permute(1, 2, 0)
                elif tensor.shape[2] == 3:
                    pass
                else:
                    raise ValueError(
                        f"Tensor shape {tensor.shape} is not supported. Expected (3, H, W) or (H, W, 3)"
                    )
            else:
                raise ValueError(f"Tensor shape {tensor.shape} is not supported.")

            print("Shape before converting to PIL:", tensor.shape)
            tensor = tensor.clamp(0, 1) * 255

            img = PIL.Image.fromarray(tensor.numpy().astype(np.uint8))
            return img

        img = tensor_to_pil(image)
        width, height = img.size
        print(f"Image size: {width}x{height}")

        draw = PIL.ImageDraw.Draw(img)

        try:
            line_color = hex_to_rgb(border_color)  # Now accessible!
        except ValueError as e:
            print(f"Error: {e}")
            return image

        h_spacing = height / (h_grids + 1)
        v_spacing = width / (v_grids + 1)

        for i in range(1, h_grids + 1):
            y = int(i * h_spacing)
            draw.line([(0, y), (width, y)], fill=line_color, width=border_width)

        for i in range(1, v_grids + 1):
            x = int(i * v_spacing)
            draw.line([(x, 0), (x, height)], fill=line_color, width=border_width)

        img_np = np.array(img).astype(np.float32) / 255.0
        print("Shape after converting from PIL:", img_np.shape)
        img_tensor = torch.from_numpy(img_np).unsqueeze(0)
        print("Final image shape:", img_tensor.shape)

        return (img_tensor,)
