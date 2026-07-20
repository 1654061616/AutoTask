"""
资源路径工具 — 开发与打包环境兼容的资源路径解析
"""
import os
import sys


def get_resource_path(relative_path):
    """
    获取资源文件的绝对路径，兼容 PyInstaller 打包和开发环境

    Args:
        relative_path: 相对于 gui/styles/resources/ 的路径

    Returns:
        资源的绝对路径
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    resource_path = os.path.join(base_path, "gui", "styles", "resources", relative_path)

    if not os.path.exists(resource_path):
        alternative_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        resource_path = os.path.join(alternative_base, "gui", "styles", "resources", relative_path)

    return resource_path


def get_resources_dir():
    """获取 resources 目录的绝对路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    resources_dir = os.path.join(base_path, "resources")

    if not os.path.exists(resources_dir):
        alternative_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        resources_dir = os.path.join(alternative_base, "resources")

    return resources_dir


def ensure_resources_dir():
    """确保 resources 目录存在，不存在则创建"""
    resources_dir = get_resources_dir()
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)
    return resources_dir


def ensure_image_dir():
    """确保 resources/image 目录存在，不存在则创建"""
    image_dir = os.path.join(get_resources_dir(), "image")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    return image_dir