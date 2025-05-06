import os
import codecs

def convert_encoding(root_dir, source_encoding='gb18030', target_encoding='utf-8'):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.m'):
                file_path = os.path.join(root, file)
                # 备份原文件（后缀 .bak）
                backup_path = file_path + '.bak'
                os.rename(file_path, backup_path)
                try:
                    # 读取 GB18030 编码内容
                    with codecs.open(backup_path, 'r', encoding=source_encoding) as f:
                        content = f.read()
                    # 写入 UTF-8 编码
                    with codecs.open(file_path, 'w', encoding=target_encoding) as f:
                        f.write(content)
                    print(f"成功转换：{file_path}")
                except Exception as e:
                    print(f"转换失败：{file_path}，错误：{str(e)}")
                    # 恢复备份文件
                    os.rename(backup_path, file_path)

if __name__ == "__main__":
    # 指定固定根目录（替换为你的实际路径）
    root_directory = r"C:\Users\32429\Desktop\计算岩土力学\3Dcode\code"
    convert_encoding(root_directory)