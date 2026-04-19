from setuptools import setup, find_packages

# 读取README.md作为长描述
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pdf-ocr-skill",
    version="2.5.0",
    author="PDF OCR Skill Team",
    author_email="",
    description="支持四引擎的PDF OCR识别技能，可从影印版PDF文件和图片文件中提取中英文文字内容 | PDF OCR Skill with quadruple-engine support, capable of extracting Chinese and English text from scanned PDF files and image files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yejinlei/pdf-ocr-skill",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pymupdf",
        "pillow",
        "requests",
        "python-dotenv"
    ],
    extras_require={
        "full": [
            "rapidocr_onnxruntime",
            "rapid-doc",
            "paddleocr"
        ]
    },
    entry_points={
        "console_scripts": [
            "pdf-ocr=scripts.pdf_ocr_processor:main",
        ],
    },
)