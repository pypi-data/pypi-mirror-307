# setup.py
from setuptools import setup, find_packages

setup(
    name="screen_text",
    version="0.1.3",
    author="",
    author_email="shmily_006@qq.com",
    description="A tool for capturing and recognizing text on screen using ddddocr and mss.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/screen_text",
    packages=find_packages(),
    install_requires=[
        "Pillow>=8.0.0,<9.0.0",     # 锁定在 Pillow 8.x.x 版本
        "mss>=6.1.0,<7.0.0",        # 锁定在 mss 6.x.x 版本
        "ddddocr>=1.3.6,<2.0.0"     # 锁定在 ddddocr 1.x.x 版本
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)