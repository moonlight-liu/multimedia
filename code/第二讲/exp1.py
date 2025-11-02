from PIL import Image
import os
import time

# 1.设置原始图片的文件名
input_filename = "original_color.jpg"

# 2.尝试打开图片
try:
  img_color = Image.open(input_filename)
  
  # 打印一些信息来确认图片已经成功加载
  print(f"图片'{input_filename}'已成功加载。")
  print(f"图片格式: {img_color.format}")
  print(f"图片大小: {img_color.size}")
  print(f"图片模式: {img_color.mode}")
  
except FileNotFoundError:
  print(f"错误：找不到文件'{input_filename}'。请确保文件存在于指定路径。")
  exit()
  
except Exception as e:
  print(f"打开图片时发生错误: {e}")
  exit()
  
# 保持这个变量供下一部分使用
print("已经成功加载图片，准备进行后续处理。")

# 转为灰度图像 (核心处理)

# 3.将彩色图片转换为灰度图片
img_gray = img_color.convert("L")

# 4.确认转换结果
print("图片已成功转换为灰度模式。")
print(f"灰度图片模式: {img_gray.mode}")


print("准备保存灰度图片。")
# 5.保存灰度图片
# 保存为PNG格式
output_png = "gray_image.png"
# 使用.save方法，pillow会根据文件扩展名自动选择编码器
# PNG格式支持无损压缩，适合保存灰度图像
img_gray.save(output_png)
print(f"灰度图片已保存为'{output_png}'。")

# 保存为BMP格式
output_bmp = "gray_image.bmp"
# BMP是一种几乎无压缩的格式，适合需要高质量图像的场景，通常文件大
img_gray.save(output_bmp)
print(f"灰度图片已保存为'{output_bmp}'。")

# 6.比较文件大小
size_png = os.path.getsize(output_png)
size_bmp = os.path.getsize(output_bmp)
print(f"文件大小比较：")
print(f"PNG文件大小 - {output_png}: {size_png} 字节")
print(f"BMP文件大小 - {output_bmp}: {size_bmp} 字节")

# 有损压缩中，一般情况下：
# 压缩比 越大（文件越小，画质越差）->运算时间 越长（压缩过程越复杂）。
# 压缩比 越小（文件越大，画质越好）-> 运算时间 越短（压缩过程越简单/轻松）。
# 原因：有损压缩通过丢弃人眼不敏感的细节数据来实现文件变小
# 压缩比小，高质量，快，只是象征性地丢弃一些细节，不需要花太多时间去分析和消除冗余信息，处理速度快
# 压缩比大，低质量，慢，需要更复杂的算法来最大化地减少文件大小，这需要更多的计算资源和时间。

# 实验验证
# 实战比较有损压缩JPEG
print("-----------------------------")
print("\n作业问题2：JPEG有损压缩比较")
print("\n比较1：高质量/低压缩比(Quality=90)")
output_jpg_high_q = "output_high_quality_90.jpg"
start_time_high = time.time()
img_color.save(output_jpg_high_q, format="JPEG", quality=90)
end_time_high = time.time()
time_high = end_time_high - start_time_high
size_high = os.path.getsize(output_jpg_high_q)
print(f"文件保存成功: {output_jpg_high_q}")
print(f"处理时间: {time_high} 秒")
print(f"文件大小: {size_high} 字节")

print("\n比较2：低质量/高压缩比(Quality=10)")
output_jpg_low_q = "output_low_quality_10.jpg"
start_time_low = time.time()
img_color.save(output_jpg_low_q, format="JPEG", quality=10)
end_time_low = time.time()
time_low = end_time_low - start_time_low
size_low = os.path.getsize(output_jpg_low_q)
print(f"文件保存成功: {output_jpg_low_q}")
print(f"处理时间: {time_low} 秒")
print(f"文件大小: {size_low} 字节")

print("\n---最终总结---")
if time_high < time_low:
    print("高质量/低压缩比的保存时间更短。")
    print(f"Q=10比Q=90多花费了 {(time_low - time_high) * 1000} 毫秒。")
else:
  print("注意：对于小图，差异可能不明显，但原则上高压缩比更耗时")