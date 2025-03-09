import os
import re
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def extract_number(filename):
    """从文件名中提取数字部分"""
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0


def create_pdf_from_images(image_folder, output_pdf):
    # 获取目录下所有图片文件
    images = [img for img in os.listdir(image_folder) if
              img.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]

    # 按文件名中的数字大小排序
    images.sort(key=extract_number)

    # 创建PDF文件
    c = canvas.Canvas(output_pdf, pagesize=A4)
    a4_width, a4_height = A4  # A4尺寸（单位为点，1点=1/72英寸）

    for image in images:
        img_path = os.path.join(image_folder, image)
        img = Image.open(img_path)
        img_width, img_height = img.size

        # 计算图片在A4页面上的位置（居中）
        x = (a4_width - img_width) / 2
        y = (a4_height - img_height) / 2

        # 如果图片尺寸超过A4，裁剪图片
        if img_width > a4_width or img_height > a4_height:
            print(f"警告：图片 {image} 尺寸超过A4，将被裁剪！")
            # 计算裁剪区域
            left = max(0, (img_width - a4_width) / 2)
            top = max(0, (img_height - a4_height) / 2)
            right = min(img_width, left + a4_width)
            bottom = min(img_height, top + a4_height)
            img = img.crop((left, top, right, bottom))
            x, y = 0, 0  # 裁剪后从左上角开始放置

        # 将图片插入PDF
        c.drawImage(img_path, x, y, width=img.width, height=img.height, preserveAspectRatio=True)
        c.showPage()  # 添加新页面

    c.save()
    print(f"PDF文件已生成: {output_pdf}")


if __name__ == "__main__":
    image_folder = "./download"  # 替换为你的图片目录
    output_pdf = "output.pdf"  # 输出的PDF文件名
    create_pdf_from_images(image_folder, output_pdf)