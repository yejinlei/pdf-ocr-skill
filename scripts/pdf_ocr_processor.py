#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF OCR处理脚本
使用硅基流动大模型进行OCR识别，处理影印版PDF文件
"""

import os
import sys
import base64
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class PDFOCRProcessor:
    """PDF OCR处理器"""
    
    def __init__(self):
        self.api_key = os.getenv("SILICON_FLOW_API_KEY", "")
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"
        # 使用专门的OCR模型
        self.model = os.getenv("SILICON_FLOW_OCR_MODEL", "deepseek-ai/DeepSeek-OCR")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def pdf_to_images(self, pdf_path: str) -> List[str]:
        """将PDF转换为图片列表（返回base64编码）"""
        try:
            import fitz  # PyMuPDF
            from PIL import Image
            import io
            
            doc = fitz.open(pdf_path)
            images = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # 将PDF页面转换为图片
                zoom = 2  # 放大倍数
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                
                # 转换为PIL Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # 转换为base64
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                images.append(img_base64)
            
            doc.close()
            return images
            
        except ImportError:
            raise Exception("请安装依赖: pip install pymupdf pillow")
        except Exception as e:
            raise Exception(f"PDF转图片失败: {str(e)}")
    
    def ocr_image(self, image_base64: str, page_num: int = 1) -> str:
        """使用硅基流动大模型识别单张图片"""
        prompt = f"""请仔细识别这张图片中的所有文字内容。
这是第 {page_num} 页的内容。

要求：
1. 完整提取所有可见文字
2. 保持文字的顺序和结构
3. 识别中文和英文
4. 输出纯文本格式，不要添加任何额外说明

请直接输出识别的文字内容："""
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.1,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=120)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"【OCR识别失败: {str(e)}】"
    
    def image_to_base64(self, image_path: str) -> str:
        """将图片文件转换为base64编码"""
        try:
            from PIL import Image
            import io
            
            # 打开图片
            img = Image.open(image_path)
            
            # 转换为RGB格式（如果需要）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 转换为base64
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            return img_base64
            
        except ImportError:
            raise Exception("请安装依赖: pip install pillow")
        except Exception as e:
            raise Exception(f"图片转base64失败: {str(e)}")
    
    def ocr_image_file(self, image_path: str) -> Dict[str, Any]:
        """OCR识别单个图片文件"""
        result = {
            "text": "",
            "page_count": 1
        }
        
        try:
            # 将图片转换为base64
            img_base64 = self.image_to_base64(image_path)
            
            # 进行OCR识别
            text = self.ocr_image(img_base64, 1)
            result["text"] = text
            
        except Exception as e:
            raise Exception(f"图片OCR识别失败: {str(e)}")
        
        return result
    
    def ocr_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """OCR识别整个PDF"""
        result = {
            "text": "",
            "page_count": 0
        }
        
        try:
            images = self.pdf_to_images(pdf_path)
            result["page_count"] = len(images)
            
            text_parts = []
            for idx, img_base64 in enumerate(images, 1):
                page_text = self.ocr_image(img_base64, idx)
                text_parts.append(f"=== 第 {idx} 页 (OCR) ===\n{page_text}")
            
            result["text"] = "\n\n".join(text_parts)
            
        except Exception as e:
            raise Exception(f"OCR识别失败: {str(e)}")
        
        return result

def process_pdf_ocr(pdf_path: str) -> Dict[str, Any]:
    """处理PDF OCR的主函数"""
    processor = PDFOCRProcessor()
    return processor.ocr_pdf(pdf_path)

if __name__ == "__main__":
    # 测试代码
    import json
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        print("使用方法: python pdf_ocr_processor.py <pdf_file_path>")
        sys.exit(1)
    
    if not os.path.exists(pdf_path):
        print(f"文件不存在: {pdf_path}")
        sys.exit(1)
    
    try:
        result = process_pdf_ocr(pdf_path)
        print(f"OCR识别完成，共 {result['page_count']} 页")
        print(f"文本长度: {len(result['text'])} 字符")
        print("\n前500字符:")
        print(result['text'][:500])
    except Exception as e:
        print(f"OCR识别失败: {str(e)}")
        sys.exit(1)