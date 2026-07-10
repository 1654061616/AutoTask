from setuptools import setup, find_packages

setup(
    name="AutoFlow",
    version="1.0.0",
    description="自动化操作软件",
    author="AutoFlow Team",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.5.0",
        "pyautogui>=0.9.54",
        "pydirectinput>=1.0.4",
        "opencv-python>=4.8.0",
        "easyocr>=1.7.0",
        "openpyxl>=3.1.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "mss>=10.0.0",
        "APScheduler>=3.10.0",
        "pyperclip>=1.8.2",
        "pywin32>=306",
        "psutil>=5.9.0",
        "keyboard>=0.13.5"
    ],
    entry_points={
        "console_scripts": [
            "autoflow=main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
)