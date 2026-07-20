"""
文件操作模块 — 封装文件和目录的常用操作
"""
import os
import shutil
import json
from typing import Dict, Any, List

class FileOperations:
    """文件操作器，支持读写、复制、移动、删除等文件与目录操作"""

    def __init__(self):
        pass

    def read_file(self, file_path: str) -> str:
        """读取文本文件内容"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_file(self, file_path: str, content: str):
        """写入文本文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def read_json(self, file_path: str) -> Dict[str, Any]:
        """读取 JSON 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_json(self, file_path: str, data: Dict[str, Any]):
        """写入 JSON 文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def append_file(self, file_path: str, content: str):
        """追加内容到文件末尾"""
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)

    def delete_file(self, file_path: str):
        """删除文件"""
        if os.path.exists(file_path):
            os.remove(file_path)

    def create_directory(self, dir_path: str):
        """创建目录（递归）"""
        os.makedirs(dir_path, exist_ok=True)

    def delete_directory(self, dir_path: str):
        """删除目录及其内容"""
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    def copy_file(self, source: str, destination: str):
        """复制文件（保留元数据）"""
        shutil.copy2(source, destination)

    def move_file(self, source: str, destination: str):
        """移动文件"""
        shutil.move(source, destination)

    def list_files(self, dir_path: str) -> List[str]:
        """列出目录中的文件"""
        return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    def list_directories(self, dir_path: str) -> List[str]:
        """列出目录中的子目录"""
        return [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

    def file_exists(self, file_path: str) -> bool:
        """判断文件是否存在"""
        return os.path.exists(file_path)

    def get_file_size(self, file_path: str) -> int:
        """获取文件大小（字节）"""
        return os.path.getsize(file_path)

    def get_file_modified_time(self, file_path: str) -> float:
        """获取文件最后修改时间戳"""
        return os.path.getmtime(file_path)