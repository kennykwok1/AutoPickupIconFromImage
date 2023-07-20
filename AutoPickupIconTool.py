import os
from PIL import Image

def find_icon_bounding_boxes(img):
    # 从图片中找到所有图标的包围盒
    icon_bounding_boxes = []
    width, height = img.size

    # 用一个二维数组记录已处理的像素
    processed_pixels = [[False for _ in range(width)] for _ in range(height)]

    for x in range(width):
        for y in range(height):
            if not processed_pixels[y][x]:
                pixel = img.getpixel((x, y))
                if pixel[3] != 0:  # 判断该像素是否不透明 (alpha 通道不为0)
                    left, top, right, bottom = find_icon_bounding_box(img, x, y, processed_pixels)
                    icon_bounding_boxes.append((left, top, right, bottom))

    return icon_bounding_boxes

def find_icon_bounding_box(img, start_x, start_y, processed_pixels):
    # 从起始点 (start_x, start_y) 开始找到一个图标的包围盒
    width, height = img.size
    left, top, right, bottom = width, height, 0, 0

    stack = [(start_x, start_y)]
    while stack:
        x, y = stack.pop()
        if 0 <= x < width and 0 <= y < height and not processed_pixels[y][x]:
            pixel = img.getpixel((x, y))
            if pixel[3] != 0:
                left = min(left, x)
                right = max(right, x)
                top = min(top, y)
                bottom = max(bottom, y)

                processed_pixels[y][x] = True

                stack.extend([(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]])

    return left, top, right, bottom

def crop_and_save_icons(input_path, output_folder):
    # 遍历 modify 目录下的 PNG 图片，找到图标并保存成单独的 PNG 文件
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_path):
        if filename.endswith(".png"):
            input_file = os.path.join(input_path, filename)

            with Image.open(input_file) as img:
                icon_bounding_boxes = find_icon_bounding_boxes(img)

                for idx, (left, top, right, bottom) in enumerate(icon_bounding_boxes):
                    icon_img = img.crop((left, top, right + 1, bottom + 1))

                    # 确保不超出图片的边界
                    new_width = right - left + 1
                    new_height = bottom - top + 1
                    if new_width > 0 and new_height > 0:
                        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_icon{idx}.png")
                        icon_img.save(output_path)

if __name__ == "__main__":
    input_folder_path = "modify"  # modify目录路径
    output_icons_folder_path = "output_icons"  # 输出图标的文件夹路径

    crop_and_save_icons(input_folder_path, output_icons_folder_path)
