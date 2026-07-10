import pytest
import sys
import os
sys.path.insert(0, '..')
from operations.file_operations import FileOperations

def test_file_operations_initialization():
    fo = FileOperations()
    assert fo is not None

def test_write_and_read_file():
    fo = FileOperations()
    test_path = "test_file.txt"
    test_content = "test content"
    fo.write_file(test_path, test_content)
    result = fo.read_file(test_path)
    assert result == test_content
    fo.delete_file(test_path)

def test_write_and_read_json():
    fo = FileOperations()
    test_path = "test_file.json"
    test_data = {"key": "value"}
    fo.write_json(test_path, test_data)
    result = fo.read_json(test_path)
    assert result == test_data
    fo.delete_file(test_path)

def test_file_exists():
    fo = FileOperations()
    test_path = "test_exists.txt"
    fo.write_file(test_path, "test")
    assert fo.file_exists(test_path)
    fo.delete_file(test_path)
    assert not fo.file_exists(test_path)

def test_create_and_delete_directory():
    fo = FileOperations()
    test_dir = "test_dir"
    fo.create_directory(test_dir)
    assert os.path.isdir(test_dir)
    fo.delete_directory(test_dir)
    assert not os.path.isdir(test_dir)