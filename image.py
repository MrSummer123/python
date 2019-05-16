from PIL import Image
# 导入图片识别包
import tesserocr
 
 
# open()方法获取要识别的图片
image = Image.open('CheckCode.png')
# 参数‘L’将图片转为灰度图像
image = image.convert('L')
# 显示图片
# image.show()
# 设置筛选值
threshold = 127
# 设置一个存放像素信息的列表
table = []
# 色域为256
for i in range(256):
    # 如果像素偏白
    if i < threshold:
        # 去除偏白的像素
        table.append(0)
    # 像素偏黑
    else:
        # 保留偏黑的像素
        table.append(1)
# 按像素信息绘制
image = image.point(table, '1')
# 显示图片
# image.show()
# image_to_text()方法将图片内容转化为文本
result = tesserocr.image_to_text(image)
# 打印转化结果
