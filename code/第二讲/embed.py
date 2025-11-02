from PIL import Image
import os
import time
import io
import itertools

# 1.将jpg图片转换为bmp图片
input_jpeg_filename = "original_color.jpg"
output_bmp_filename = "original_color.bmp"

# 打开JPEG图片并转换为BMP格式
try:
    img = Image.open(input_jpeg_filename)
    img.save(output_bmp_filename, "BMP")
    print(f"成功将'{input_jpeg_filename}'转换为'{output_bmp_filename}'。")
except Exception as e:
    print(f"转换过程中发生错误: {e}")
    
# 将字符串转换为二进制列表
def text_bits(text):
  """将字符串转换为二进制列表"""
  bits = []
  # 将每一个字符转换为8位二进制
  for char in text:
    # ord(char)获取字符ASCII码
    # bin()转换为二进制字符串，前面有0b的前缀
    # 使用zfill(8)确保是8位，不足补0
    binary_char = bin(ord(char))[2:].zfill(8)
    bits.extend(list(binary_char))
  return bits

# 核心函数 嵌入信息
def embed_message(input_bmp_filename,message_to_hide,output_bmp_filename):
  # 1.设置终止符和准备数据
  TERMINATOR = "$$$"
  full_message = message_to_hide + TERMINATOR
  message_bits = text_bits(full_message)
  
  # 计算所需的像素数，每个像素的R通道嵌入1为，所有需要和位数一样多的像素
  required_pixels = len(message_bits)
  
  print(f"需要嵌入的总位数: {len(message_bits)}，需要的像素数: {required_pixels}")
  
  # 2.加载BMP图片并转换为可操作的像素数据
  try:
    img = Image.open(input_bmp_filename)
  except FileNotFoundError:
    print(f"错误：找不到文件'{input_bmp_filename}'。请确保文件存在于指定路径。")
    return
  
  # 确保图片是RGB模式，否则无法访问RGB三个通道
  if img.mode != "RGB":
    print(f"图片模式为'{img.mode}'，正在转换为'RGB'模式。")
    img = img.convert("RGB")
    
  width,height = img.size
  total_poxels = width * height
  
  if required_pixels > total_poxels:
    print(f"错误：图片像素数({total_poxels})不足以嵌入所需信息({required_pixels}像素)。")
    return
  
  # 用于修改像素的列表
  pixels = list(img.getdata())
  new_pixels = []
  
  # 3.循环嵌入信息
  # 使用itertools.zip_longest确保遍历所有消息位
  message_iterator = iter(message_bits)
  for i,pixel in enumerate(pixels):
    R,G,B = pixel
    
    # 尝试从信息位中获取下一位
    try:
      bit_to_embed_str = next(message_iterator)
      bit_to_embed = int(bit_to_embed_str)
      
      # LSB嵌入操作
      # 清除R通道的最低位
      R_cleared = R & 0b11111110
      # 设置R通道的最低位为要嵌入的位
      R_embedded = R_cleared | bit_to_embed
      # 构造新的像素
      new_pixel = (R_embedded,G,B)
    except StopIteration:
      # 信息位嵌入完毕，后续像素不变
      new_pixel = pixel
    new_pixels.append(new_pixel)
    
  # 4.创建新图片并保存
  img_stego = Image.new(img.mode,img.size)
  img_stego.putdata(new_pixels)
  img_stego.save(output_bmp_filename)
  print(f"嵌入信息后的图片已保存为'{output_bmp_filename}'")
  
#调用
embed_message("original_color.bmp","This is my first multimedia experiment.","stego_image.bmp")
print("信息嵌入完成。")

# 信息提取
def extract_message(stego_bmp_filename):
  TERMINATOR = "$$$"
  extracted_bits = []
  
  # 1.加载嵌入信息后的BMP图片
  try:
    img = Image.open(stego_bmp_filename)
  except FileNotFoundError:
    print(f"错误：找不到文件'{stego_bmp_filename}'。请确保文件存在于指定路径。")
    return ""
  
  # 确保图片是RGB模式
  if img.mode != "RGB":
    print(f"图片模式为'{img.mode}'，正在转换为'RGB'模式。")
    img = img.convert("RGB")
    
  pixels = list(img.getdata())
  
  # 2.循环提取信息位
  for pixel in pixels:
    R,G,B = pixel
    # 提取R通道的最低位
    lsb = R & 0b00000001
    extracted_bits.append(str(lsb))
    
    if len(extracted_bits) % 8 != 0:
      continue  # 每8位处理一次
  
    BITS_PER_CHAR = 8
    # 3.检查终止符
    current_byte_str = "".join(extracted_bits[-8:])
    char_code = int(current_byte_str,2)
    current_char = chr(char_code)
    # 提取的字符序列长度必须达到终止长度才能检查
    if len(extracted_bits) // BITS_PER_CHAR >= len(TERMINATOR):
      # 检查已提取的最后几个字符是否为终止符
      full_extracted_bytes = "".join(extracted_bits)
      extracted_chars = ""
      
      # 每8位处理一次
      for i in range(0,len(full_extracted_bytes),BITS_PER_CHAR):
        byte_str = full_extracted_bytes[i:i+BITS_PER_CHAR]
        char_code = int(byte_str,2)
        extracted_chars += chr(char_code)
        
      # 检查终止符
      if extracted_chars.endswith(TERMINATOR):
        # 找到了！移除终止符并返回结果
        final_message = extracted_chars[:-len(TERMINATOR)]
        print("成功提取到隐藏信息。")
        return final_message
  print("未找到终止符，可能信息不完整。")
  return None

message = extract_message("stego_image.bmp")
if message is not None:
  print(f"提取的信息为: {message}")
# 信息提取调用结束
print("信息提取完成。")
    