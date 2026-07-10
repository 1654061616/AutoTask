import os
import shutil
import json
from typing import Dict, Any, List

class FileOperations:
    def __init__(self):
        pass
    
    def read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def write_file(self, file_path: str, content: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def read_json(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def write_json(self, file_path: str, data: Dict[str, Any]):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def append_file(self, file_path: str, content: str):
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
    
    def delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def create_directory(self, dir_path: str):
        os.makedirs(dir_path, exist_ok=True)
    
    def delete_directory(self, dir_path: str):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    
    def copy_file(self, source: str, destination: str):
        shutil.copy2(source, destination)
    
    def move_file(self, source: str, destination: str):
        shutil.move(source, destination)
    
    def list_files(self, dir_path: str) -> List[str]:
        return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    
    def list_directories(self, dir_path: str) -> List[str]:
        return [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    
    def file_exists(self, file_path: str) -> bool:
        return os.path.exists(file_path)
    
    def get_file_size(self, file_path: str) -> int:
        return os.path.getsize(file_path)
    
    def get_file_modified_time(self, file_path: str) -> float:
        return os.path.getmtime(file_path)