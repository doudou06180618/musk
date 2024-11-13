import os

class TableFinder:
    def __init__(self, root_dir, exclude_dirs, file_to_check):
        self.root_dir = root_dir
        self.exclude_dirs = exclude_dirs
        self.file_to_check = file_to_check
        self.table_names = set()
        self.found_tables = {}  # 用字典存储找到的表名及其对应路径

    def load_table_names(self):
        """从指定的文件中加载表名"""
        try:
            with open(self.file_to_check, 'r') as f:
                self.table_names = {line.strip() for line in f if line.strip()}
        except FileNotFoundError:
            print(f"错误: 文件 {self.file_to_check} 未找到.")
            return False
        return True

    def traverse_directory(self):
        """遍历目录并查找表名"""
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            # 跳过排除目录
            if any(os.path.commonpath([dirpath, excl]) == excl for excl in self.exclude_dirs):
                continue

            # 检查每个文件内容是否包含表名
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)

                # 跳过对文件本身的检查
                if os.path.abspath(self.file_to_check) == file_path or \
                        file_path == os.path.abspath(self.exclude_dirs[len(self.exclude_dirs) - 1]):  # 获取最后一个排除文件
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        for table in self.table_names:
                            if table in content:
                                if table not in self.found_tables:
                                    self.found_tables[table] = []
                                self.found_tables[table].append(file_path)
                except (UnicodeDecodeError, PermissionError):
                    continue

    def print_found_tables(self):
        """打印找到的表名及其对应路径"""
        if self.found_tables:
            print("以下表在指定目录中出现过，并对应的文件路径:")
            for table, paths in self.found_tables.items():
                print(f"表名: {table} -> 文件路径: {', '.join(paths)}")
        else:
            print("没有找到任何表名.")

    def execute(self):
        """执行完整的查找流程"""
        if self.load_table_names():
            self.traverse_directory()
            self.print_found_tables()

    def run(self):
        """直接执行查找过程的方法"""
        self.execute()


# 使用示例
if __name__ == "__main__":
    root_directory = r"D:\code\docu\bi-core\sh"
    excluded_directories = [
        r"D:\code\docu\bi-core\sh\sbin\etl\full",
        r"D:\code\docu\bi-core\sh\sbin\etl\part",
        r"D:\code\docu\bi-core\sh\sbin\compute_stats\databases_file",
        r"D:\code\docu\bi-core\sh\sbin\etl\currency",
        r"D:\code\docu\bi-core\sh\sbin\other_use\5bi.txt"  # 排除 5bi.txt 文件
    ]
    file_to_check = r"D:\code\docu\bi-core\sh\sbin\other_use\6bi.txt"

    table_finder = TableFinder(root_directory, excluded_directories, file_to_check)
    table_finder.run()  # 直接调用 run() 方法执行查找过程
