# WatermarkRemover-AI

**基于 Florence-2 和 LaMA 模型的 AI 智能水印去除工具**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![CUDA Support](https://img.shields.io/badge/CUDA-12.4-green.svg)](https://developer.nvidia.com/cuda-toolkit)

[English](README.md) | 简体中文

---

## 📖 概述

`WatermarkRemover-AI` 是一款先进的 AI 水印去除应用程序，利用深度学习模型实现精准的水印检测和无缝去除。特别适用于去除 Sora、Sora 2、Runway 等 AI 生成视频中的水印。

本项目使用 Microsoft 的 Florence-2 模型进行水印识别，使用 LaMA (Large Mask Inpainting) 模型进行图像修复，并配备基于 PyWebview 的现代化图形界面，提供直观便捷的用户体验。

## 📸 截图预览

![应用截图](assets/screenshot-preview.png)

## 🎬 演示视频

https://github.com/user-attachments/assets/505be2a8-8eda-4def-90b6-5a4ceefee456

---

## ✨ 功能特性

- **🎯 智能检测** - 基于 Florence-2 的 AI 水印检测
- **🔧 无缝去除** - LaMA 图像修复技术实现自然效果
- **🎥 视频支持** - 支持双通道检测和音频保留
- **🤖 AI 视频适配** - 专门优化去除 Sora、Sora 2、Runway 等 AI 生成视频的水印
- **📁 批量处理** - 一键处理整个文件夹
- **👁️ 预览模式** - 处理前预览检测到的水印
- **🌅 淡入淡出处理** - 智能处理渐变出现/消失的水印
- **⚡ GPU 加速** - CUDA 支持，显著提升处理速度

---

## 🛠️ 安装指南

### Windows 系统

安装脚本会自动下载便携式 Python 环境，无需系统预装 Python。

```powershell
git clone https://github.com/D-Ogi/WatermarkRemover-AI.git
cd WatermarkRemover-AI
.\setup.ps1
```

安装完成后，双击 `run.bat` 启动应用。

### Linux / macOS 系统

需要系统已安装 Python 3.10 或更高版本。

```bash
git clone https://github.com/D-Ogi/WatermarkRemover-AI.git
cd WatermarkRemover-AI
chmod +x setup.sh
./setup.sh
```

安装完成后：
```bash
source venv/bin/activate
python remwmgui.py
```

### 可选：安装 FFmpeg

安装 FFmpeg 以在处理视频时保留音频：
- **Windows**: 从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载并添加到 PATH
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

---

## 📖 使用说明

### 图形界面模式

1. 运行应用程序（Windows 双击 `run.bat`，或执行 `python remwmgui.py`）
2. 选择处理模式（单文件或批量处理）
3. 设置输入和输出路径
4. 根据需要配置参数
5. 点击 **LET HIM COOK** 开始处理

### 命令行模式

```bash
# 基础用法
python remwm.py input.png output_folder/

# 带参数使用
python remwm.py ./images ./output --overwrite --max-bbox-percent=15 --force-format=PNG

# 处理视频（双通道检测）
python remwm.py video.mp4 ./output --detection-skip=3 --fade-in=0.5 --fade-out=0.5

# 预览模式（仅检测不处理）
python remwm.py input.png --preview
```

### 命令行参数说明

| 参数 | 说明 |
|------|------|
| `--overwrite` | 覆盖已存在的文件 |
| `--transparent` | 将水印区域设为透明（仅图片） |
| `--max-bbox-percent` | 检测框最大占图片比例（默认：10%） |
| `--force-format` | 强制输出格式（PNG, WEBP, JPG, MP4, AVI） |
| `--detection-prompt` | 自定义检测提示词（默认："watermark"） |
| `--detection-skip` | 视频每N帧检测一次（1-10，默认：1） |
| `--fade-in` | 向前扩展遮罩N秒（处理淡入水印） |
| `--fade-out` | 向后扩展遮罩N秒（处理淡出水印） |
| `--preview` | 预览模式，仅检测不处理 |

---

## 🎥 视频处理说明

- **支持格式：** MP4, AVI, MOV, MKV, FLV, WMV, WEBM
- **音频保留：** 需要安装 FFmpeg
- **双通道模式：** 使用 `--detection-skip` > 1 可加快处理速度
- **渐变处理：** 使用 `--fade-in` / `--fade-out` 处理渐变出现/消失的水印

---

## 🔧 技术栈

- **Florence-2** - 微软视觉模型，用于水印检测
- **LaMA** - 大型遮罩图像修复模型
- **PyWebview** - 跨平台 Webview 封装
- **Alpine.js** - 轻量级 JavaScript UI 框架
- **PyTorch** - 深度学习后端

---

## 🤝 参与贡献

欢迎贡献代码！您可以：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📄 许可证

本项目基于 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件

---

## ⭐ 致谢

- [Microsoft Florence-2](https://huggingface.co/microsoft/Florence-2-large) - 视觉模型
- [LaMA](https://github.com/saic-mdal/lama) - 图像修复模型
- [IOPaint](https://github.com/Sanster/IOPaint) - 图像修复工具库

---

## 📞 联系方式

如有问题或建议，请通过 [Issues](https://github.com/D-Ogi/WatermarkRemover-AI/issues) 提交。
