import os
import shutil

def merge_images(source_folder, target_folder, move=False):
    """
    将源文件夹中所有子文件夹的图片合并到目标文件夹
    
    参数:
    source_folder (str): 源文件夹路径
    target_folder (str): 目标文件夹路径
    move (bool): 是否移动文件（默认False即复制）
    """
    # 支持的图片扩展名
    image_extensions = {'.jpg', '.arw','.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    
    # 创建目标文件夹（如果不存在）
    os.makedirs(target_folder, exist_ok=True)
    
    # 遍历所有子文件夹
    for root, _, files in os.walk(source_folder):
        for filename in files:
            # 获取文件扩展名并转为小写
            ext = os.path.splitext(filename)[1].lower()
            
            if ext in image_extensions:
                # 原始文件完整路径
                src_path = os.path.join(root, filename)
                
                # 目标文件基础路径
                base_name = os.path.splitext(filename)[0]
                dst_path = os.path.join(target_folder, filename)
                
                # 处理重名文件
                counter = 1
                while os.path.exists(dst_path):
                    # 如果文件已存在，添加序号
                    new_name = f"{base_name}_{counter}{ext}"
                    dst_path = os.path.join(target_folder, new_name)
                    counter += 1
                
                # 复制/移动文件
                if move:
                    shutil.move(src_path, dst_path)
                    print(f"Moved: {src_path} -> {dst_path}")
                else:
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied: {src_path} -> {dst_path}")

if __name__ == "__main__":
    # 使用示例
    source = "D:\Myfile\MyFile\Camera\ZVE_10"  # 替换为你的源文件夹路径
    target = "D:\Myfile\MyFile\Camera\ZVE_10"  # 替换为你的目标文件夹路径
    
    merge_images(source, target, move=True)  # 使用move=True会移动文件