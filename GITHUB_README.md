# 🎬 Video Smart Editor

**视频智能剪辑工具 - 基于语义理解的自动化视频剪辑**

[![Version](https://img.shields.io/badge/version-3.0-blue.svg)](https://github.com/dys-cq/video-smart-editor/releases/tag/v3.0)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

---

## 📖 项目简介

Video Smart Editor 是一个基于语义理解的自动化视频剪辑工具，支持：

- 🎙️ **语音转录** - 使用 Whisper 生成带时间戳的 SRT 字幕
- 📜 **字幕嵌入** - 使用 FFmpeg 将字幕硬编码到视频
- 🧠 **语义分析** - 自动检测语气词、过短片段、重复内容
- 📊 **报告生成** - 生成审稿报告 (Markdown) 和剪辑明细 (CSV)

---

## ✨ 核心功能

### 1. 语音转录
- 支持多种 Whisper 模型 (tiny/base/small/medium/large)
- 自动生成带时间戳的 SRT 字幕
- 支持中文、英文等多种语言

### 2. 字幕嵌入
- FFmpeg 硬编码字幕到视频
- 可自定义字体、字号、颜色、位置
- 默认微软雅黑 24 号字，白色 + 黑边

### 3. 语义分析
- **语气词检测**: "嗯"、"啊"、"这个"、"就是"等
- **过短片段**: <0.5 秒的片段
- **重复内容**: 完全重复的语句

### 4. 报告生成
- **审稿报告**: Markdown 格式，包含问题列表和优化建议
- **剪辑明细**: CSV 格式，详细记录每个问题点

---

## 🚀 快速开始

### 安装依赖

```bash
# 确保已安装 FFmpeg
ffmpeg -version

# 安装 Python 依赖
uv pip install openai-whisper
```

### 使用方法

```bash
# 克隆仓库
git clone https://github.com/dys-cq/video-smart-editor.git
cd video-smart-editor

# 配置输入视频（编辑 video_editor.py）
# 修改 INPUT_DIR 和 VIDEO_NAME

# 运行脚本
uv run python video_editor.py
```

### 输出文件

```
output/
├── {视频名}_精简版.mp4      # 嵌入字幕的视频
├── {视频名}_字幕.srt         # SRT 字幕文件
├── {视频名}_审稿报告.md      # 语义分析报告
└── {视频名}_剪辑明细.csv     # 剪辑点详细记录
```

---

## 📊 测试案例

### 输入视频
- **文件**: `日报助手.mov`
- **时长**: 278.6 秒 (4 分 38 秒)
- **大小**: 109.7 MB

### 处理结果
- ✅ **字幕片段**: 154 个
- ✅ **检测问题**: 7 处语气词
- ✅ **输出视频**: 20.24 MB (已嵌入字幕)
- ✅ **可节省时长**: ~7 秒 (2.5%)

### 检测到的语气词

| 时间 | 内容 | 建议 |
|------|------|------|
| 00:01:43 | "这个" | 删除 |
| 00:01:58 | "就是" | 删除 |
| 00:02:35 | "对不对" | 删除 |
| 00:03:32 | "来去" | 删除 |
| 00:04:19 | "可以" | 删除 |
| 00:04:22 | "就是" | 删除 |
| 00:04:35 | "好" | 删除 |

---

## ⚙️ 配置说明

### 基础配置

编辑 `video_editor.py` 顶部：

```python
INPUT_DIR = Path(r"E:\video_input")      # 输入目录
VIDEO_NAME = "日报助手"                   # 视频文件名
WHISPER_MODEL = "base"                   # Whisper 模型
WHISPER_LANGUAGE = "zh"                  # 语言
```

### 字幕样式

```python
force_style='FontName=Microsoft YaHei,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=1,Align=2'
```

### 语气词列表

```python
filler_words = ['嗯', '啊', '这个', '那个', '然后', '就是', '好', '可以', '来去', '对不对']
```

---

## 📚 文档

- [SKILL.md](SKILL.md) - 技能标准文档
- [README.md](README.md) - 详细使用指南
- [UPDATE_REPORT.md](UPDATE_REPORT.md) - 更新报告
- [GIT_VERSION_CONTROL.md](GIT_VERSION_CONTROL.md) - 版本管理说明

---

## 🔧 技术栈

- **Python 3.8+** - 主要编程语言
- **Whisper** - 语音识别引擎
- **FFmpeg** - 视频处理和字幕嵌入
- **OpenClaw** - 技能运行平台

---

## 📋 系统要求

- **操作系统**: Windows 10/11, macOS, Linux
- **Python**: 3.8 或更高版本
- **FFmpeg**: 已安装并添加到 PATH
- **内存**: 至少 4GB RAM (Whisper 模型需要)
- **磁盘**: 至少 1GB 可用空间

---

## 🎯 适用场景

### ✅ 最佳适用
- 口播视频自动剪辑
- 日报/周报视频生成
- 教学视频精剪
- 会议录像整理
- 播客视频化

### ❌ 不适用
- 纯音乐视频
- 多对话场景（如访谈）
- 需要复杂特效的视频

---

## 📈 版本历史

### v3.0 (2026-03-24)
- ✅ 实现语音转录生成 SRT 字幕
- ✅ 实现字幕硬编码嵌入视频
- ✅ 实现语义分析检测语气词
- ✅ 生成审稿报告和剪辑明细
- ✅ 添加完整的文档

### v2.0 (实验版本)
- ⚠️ 尝试自动剪辑但 FFmpeg 滤镜过于复杂

### v1.0 (初始版本)
- 🎉 基础语音转录
- 📝 简单语义分析

---

## 🐛 常见问题

### Q: 字幕无法嵌入？

**A**: 确保：
1. FFmpeg 已正确安装
2. 从技能目录执行（使用相对路径）
3. 字幕文件编码为 UTF-8

### Q: Whisper 识别不准确？

**A**: 尝试更大的模型：
```python
WHISPER_MODEL = "medium"  # 或 "large"
```

### Q: 如何检测更多语气词？

**A**: 编辑 `filler_words` 列表添加自定义词

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 📞 联系方式

- **GitHub**: [@dys-cq](https://github.com/dys-cq)
- **项目地址**: https://github.com/dys-cq/video-smart-editor
- **问题反馈**: https://github.com/dys-cq/video-smart-editor/issues

---

## 🙏 致谢

- [OpenAI Whisper](https://github.com/openai/whisper) - 语音识别引擎
- [FFmpeg](https://ffmpeg.org/) - 视频处理工具
- [OpenClaw](https://github.com/openclaw/openclaw) - 技能平台

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

*Video Smart Editor v3.0 - 让视频剪辑更智能*
