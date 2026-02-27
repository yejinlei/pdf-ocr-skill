---
name: pdf-ocr
description: 使用硅基流动大模型进行OCR识别，支持从影印版PDF文件和图片文件中提取文字内容
version: 1.0.0
author: PDF OCR Skill Team
license: MIT
tags:
  - ocr
  - pdf
  - image
  - text-extraction
  - chinese
  - english
  - siliconflow
  - deepseek
---

# PDF OCR Skill

PDF OCR技能用于从影印版PDF文件和图片文件中提取文字内容。该技能使用硅基流动大模型进行光学字符识别（OCR），能够识别扫描版PDF和图片中的中文和英文文字。

## 功能特性

- 支持影印版PDF文件的文字提取
- 支持多种图片格式的文字识别（JPG、PNG、BMP、GIF、TIFF、WEBP）
- 使用硅基流动大模型进行OCR识别
- 支持中文和英文文字识别
- 保持文字的顺序和结构
- 自动将PDF页面转换为图片进行识别

## 安装

### 依赖要求

```bash
pip install pymupdf pillow requests python-dotenv
```

### 环境变量配置

1. 复制 `.env.example` 文件并重命名为 `.env`
2. 填入您的硅基流动 API 密钥：

```env
SILICON_FLOW_API_KEY=your_api_key_here
SILICON_FLOW_OCR_MODEL=deepseek-ai/DeepSeek-OCR
```

## 快速开始

### 识别PDF文件

```python
# 导入OCR处理器
from pdf_ocr_processor import PDFOCRProcessor

# 创建处理器实例
processor = PDFOCRProcessor()

# 执行PDF OCR识别
result = processor.ocr_pdf('path/to/your/scanned.pdf')

# 获取识别结果
print(f"识别完成，共 {result['page_count']} 页")
print(result['text'])
```

### 识别图片文件

```python
# 导入OCR处理器
from pdf_ocr_processor import PDFOCRProcessor

# 创建处理器实例
processor = PDFOCRProcessor()

# 执行图片OCR识别
result = processor.ocr_image_file('path/to/your/image.jpg')

# 获取识别结果
print(f"识别结果: {result['text']}")
```

## 支持的文件格式

- **PDF文件**: .pdf
- **图片文件**: .jpg, .jpeg, .png, .bmp, .gif, .tiff, .webp

## 输出格式

```python
{
    "text": "识别的完整文本内容",
    "page_count": 页数  # 图片文件始终为1
}
```

## 使用场景

- 处理扫描版合同、协议等文档
- 提取影印版书籍、报告中的文字
- 处理无法直接复制文字的PDF文件
- 批量处理扫描版PDF文档
- 识别截图、扫描件等图片中的文字
- 处理手写体或印刷体图片文字识别

## 注意事项

1. OCR识别需要调用硅基流动API，可能会产生费用
2. 识别速度取决于文件页数、图片大小和网络状况
3. 对于复杂的扫描版PDF或图片，识别准确率可能会有所不同
4. 建议使用高清晰度的扫描版PDF或图片以获得更好的识别效果

## 许可证

MIT License - 详见 [LICENSE.txt](LICENSE.txt)