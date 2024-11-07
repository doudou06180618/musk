import os

class FileLister:
    def __init__(self, directory):
        self.directory = directory

    def get_file_names(self):
        """获取指定目录下所有文件的名称，以逗号分隔的字符串返回"""
        try:
            # 获取文件名称并用逗号隔开
            files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
            return ','.join(files)
        except FileNotFoundError:
            print(f"错误：路径 '{self.directory}' 未找到。")
            return ""
        except PermissionError:
            print(f"错误：没有权限访问路径 '{self.directory}'。")
            return ""

    def run(self):
        """执行文件列表获取并打印"""
        file_names = self.get_file_names()
        if file_names:
            print("文件列表:")
            print(file_names)
        else:
            print("指定目录下没有找到任何文件或出现错误。")


# 使用示例
if __name__ == "__main__":
    directory = r"D:\code\hb\bi-core\job\bi-core\etl\part"
    file_lister = FileLister(directory)
    file_lister.run()
