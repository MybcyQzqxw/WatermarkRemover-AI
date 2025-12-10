"""
批量图片水印去除脚本
Batch Watermark Removal Script

用法 / Usage:
    python batch_remove_watermark.py <输入文件夹> <输出文件夹> [选项]
    python batch_remove_watermark.py ./input_images ./output_images

功能 / Features:
    - 从指定文件夹读取所有jpg图片
    - 使用AI自动检测并去除水印
    - 保留原始文件名存储到输出文件夹
"""

import sys
import os
from pathlib import Path

# 确保当前目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import click
import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from loguru import logger

# Monkey-patch for huggingface_hub compatibility
import huggingface_hub
if not hasattr(huggingface_hub, 'cached_download'):
    huggingface_hub.cached_download = huggingface_hub.hf_hub_download

from transformers import AutoProcessor, Florence2ForConditionalGeneration


def load_models(device: str):
    """加载 Florence-2 和 LaMA 模型"""
    logger.info("正在加载 Florence-2 模型...")
    florence_model = Florence2ForConditionalGeneration.from_pretrained(
        "florence-community/Florence-2-large"
    ).to(device).eval()
    florence_processor = AutoProcessor.from_pretrained("florence-community/Florence-2-large")
    logger.info("Florence-2 模型加载完成")
    
    logger.info("正在加载 LaMA 模型...")
    # 导入本地模块
    from remwm import load_lama_model
    model_manager = load_lama_model(device)
    logger.info("LaMA 模型加载完成")
    
    return florence_model, florence_processor, model_manager


def process_single_image(
    image_path: Path,
    output_path: Path,
    florence_model,
    florence_processor,
    model_manager,
    device: str,
    max_bbox_percent: float = 10.0,
    detection_prompt: str = "watermark"
):
    """处理单张图片"""
    from remwm import get_watermark_mask, process_image_with_lama
    
    try:
        # 加载图片
        pil_image = Image.open(image_path).convert("RGB")
        
        # 获取水印遮罩
        mask_image = get_watermark_mask(
            pil_image, 
            florence_model, 
            florence_processor, 
            device, 
            max_bbox_percent, 
            detection_prompt
        )
        
        # 检查是否检测到水印
        mask_array = np.array(mask_image)
        if mask_array.max() == 0:
            # 没有检测到水印，直接复制原图
            pil_image.save(output_path)
            return True, "未检测到水印，保存原图"
        
        # 使用 LaMA 进行图像修复
        import cv2
        lama_result = process_image_with_lama(
            np.array(pil_image), 
            mask_array, 
            model_manager
        )
        
        # 保存结果
        result_image = Image.fromarray(cv2.cvtColor(lama_result, cv2.COLOR_BGR2RGB))
        result_image.save(output_path)
        
        return True, "处理成功"
        
    except Exception as e:
        logger.error(f"处理图片 {image_path} 时出错: {str(e)}")
        return False, str(e)


@click.command()
@click.argument("input_folder", type=click.Path(exists=True))
@click.argument("output_folder", type=click.Path())
@click.option("--max-bbox-percent", default=10.0, help="检测框最大占图片比例 (默认: 10%)")
@click.option("--detection-prompt", default="watermark", help="水印检测提示词 (默认: watermark)")
@click.option("--overwrite", is_flag=True, help="覆盖已存在的输出文件")
@click.option("--extensions", default="jpg,jpeg,png,webp", help="处理的图片格式 (默认: jpg,jpeg,png,webp)")
def main(
    input_folder: str,
    output_folder: str,
    max_bbox_percent: float,
    detection_prompt: str,
    overwrite: bool,
    extensions: str
):
    """
    批量去除图片水印
    
    INPUT_FOLDER: 输入图片文件夹路径
    OUTPUT_FOLDER: 输出图片文件夹路径
    
    示例:
        python batch_remove_watermark.py ./watermarked_images ./clean_images
        python batch_remove_watermark.py ./input ./output --max-bbox-percent=15 --overwrite
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # 创建输出文件夹
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 解析扩展名
    ext_list = [f".{ext.strip().lower()}" for ext in extensions.split(",")]
    
    # 获取所有图片文件
    image_files = []
    for ext in ext_list:
        image_files.extend(input_path.glob(f"*{ext}"))
        image_files.extend(input_path.glob(f"*{ext.upper()}"))
    
    # 去重
    image_files = list(set(image_files))
    image_files.sort()
    
    if not image_files:
        logger.error(f"在 {input_folder} 中未找到支持的图片文件 ({extensions})")
        return
    
    logger.info(f"找到 {len(image_files)} 张图片待处理")
    
    # 检测设备
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"使用设备: {device}")
    
    if device == "cpu":
        logger.warning("警告: 使用 CPU 处理会非常慢，建议使用支持 CUDA 的 GPU")
    
    # 加载模型
    florence_model, florence_processor, model_manager = load_models(device)
    
    # 处理统计
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    # 批量处理
    print("\n" + "="*60)
    print("开始批量处理图片水印去除")
    print("="*60 + "\n")
    
    for image_file in tqdm(image_files, desc="处理进度"):
        output_file = output_path / image_file.name
        
        # 检查是否跳过
        if output_file.exists() and not overwrite:
            logger.info(f"跳过已存在的文件: {output_file.name}")
            skip_count += 1
            continue
        
        # 处理图片
        success, message = process_single_image(
            image_file,
            output_file,
            florence_model,
            florence_processor,
            model_manager,
            device,
            max_bbox_percent,
            detection_prompt
        )
        
        if success:
            success_count += 1
            logger.info(f"✓ {image_file.name} -> {output_file.name} ({message})")
        else:
            fail_count += 1
            logger.error(f"✗ {image_file.name}: {message}")
    
    # 打印统计结果
    print("\n" + "="*60)
    print("处理完成!")
    print("="*60)
    print(f"  成功: {success_count} 张")
    print(f"  跳过: {skip_count} 张")
    print(f"  失败: {fail_count} 张")
    print(f"  输出目录: {output_path.absolute()}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
