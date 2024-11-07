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
            if any(os.path.abspath(dirpath).startswith(os.path.abspath(excl)) for excl in self.exclude_dirs):
                continue

            # 检查每个文件内容是否包含表名
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)

                # 跳过对文件本身的检查
                if os.path.abspath(self.file_to_check) == file_path or \
                        os.path.abspath(file_path) == os.path.abspath(self.exclude_dirs[-1]):  # 直接排除最后一个排除文件
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        for table in self.table_names:
                            if table in content:
                                if table not in self.found_tables:
                                    self.found_tables[table] = []
                                self.found_tables[table].append(file_path)
                except (UnicodeDecodeError, PermissionError):
                    continue

    def find_missing_tables(self):
        """找出未出现的表名并返回"""
        return self.table_names - self.found_tables.keys()

    def print_missing_tables(self):
        """打印未出现的表名"""
        not_found_tables = self.find_missing_tables()
        if not_found_tables:
            print("以下表在指定目录中没有出现过:")
            for table in not_found_tables:
                print(table)
        else:
            print("所有表名均已找到.")

    def print_found_tables(self):
        """打印找到的表名及其对应路径"""
        if self.found_tables:
            print("以下表已找到，并对应的文件路径:")
            for table, paths in self.found_tables.items():
                print(f"表名: {table} -> 文件路径: {', '.join(paths)}")
        else:
            print("没有找到任何表名.")

    def execute(self):
        """执行完整的查找流程"""
        if self.load_table_names():
            self.traverse_directory()
            self.print_missing_tables()
            self.print_found_tables()

    def get_found_tables(self):
        """获取已找到的表名及其路径"""
        return self.found_tables

    def get_all_table_names(self):
        """获取所有表名"""
        return self.table_names

    def reset(self):
        """重置表名和已找到的表名"""
        self.table_names.clear()
        self.found_tables.clear()

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
        r"D:\code\docu\bi-core\sh\sbin\other_use\5bi.txt",
        r"D:\code\docu\bi-core\sh\sbin\other_use\6bi.txt"
    ]
    file_to_check = r"D:\code\docu\bi-core\sh\sbin\other_use\5bi.txt"

    table_finder = TableFinder(root_directory, excluded_directories, file_to_check)
    table_finder.run()  # 直接调用 run() 方法执行查找过程
