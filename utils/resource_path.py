import os
import sys


def get_resource_path(relative_path):
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
    resources_dir = get_resources_dir()
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)
    return resources_dir


def ensure_image_dir():
    image_dir = os.path.join(get_resources_dir(), "image")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    return image_dir