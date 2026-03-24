# Video Smart Editor - 视频智能剪辑工具

🎬 基于语义理解的自动化视频剪辑工具

---

## 📦 安装

### 1. 系统依赖

确保已安装 FFmpeg：

```bash
ffmpeg -version
```

如未安装，访问 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载

### 2. Python 依赖

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\video_smart_editor
uv pip install openai-whisper
```

---

## 🚀 快速开始

### 步骤 1: 准备视频

将视频文件放入 `E:\video_input\` 目录，例如：
```
E:\video_input\日报助手.mov
```

### 步骤 2: 运行脚本

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\video_smart_editor
uv run python scripts/video_editor.py
```

### 步骤 3: 查看输出

处理完成后，在 `E:\video_input\output\` 目录查看：

```
E:\video_input\output\
├── 日报助手_精简版.mp4      ← 嵌入字幕的视频
├── 日报助手_字幕.srt         ← SRT 字幕文件
├── 日报助手_审稿报告.md      ← 语义分析报告
└── 日报助手_剪辑明细.csv     ← 剪辑点详细记录
```

---

## ⚙️ 配置说明

编辑 `video_editor.py` 顶部的配置区域：

```python
# 输入输出目录
INPUT_DIR = Path(r"E:\video_input")
OUTPUT_DIR = INPUT_DIR / "output"
WORK_DIR = INPUT_DIR / "work"

# 视频文件名（不含扩展名）
VIDEO_NAME = "日报助手"

# Whisper 模型配置
WHISPER_MODEL = "base"  # tiny/base/small/medium/large
WHISPER_LANGUAGE = "zh"  # zh/en/ja 等
```

---

## 📊 输出说明

### 1. 精简版视频 (`_精简版.mp4`)

- **格式**: MP4 (H.264 视频 + AAC 音频)
- **字幕**: 硬编码嵌入（微软雅黑 24 号）
- **特点**: 可直接上传到视频平台

### 2. SRT 字幕 (`_字幕.srt`)

- **格式**: SubRip 字幕
- **内容**: 带时间戳的完整字幕
- **用途**: 可编辑、可翻译、可用于其他视频

### 3. 审稿报告 (`_审稿报告.md`)

- **格式**: Markdown
- **内容**: 
  - 视频基本信息
  - 检测到的问题列表
  - 优化建议

### 4. 剪辑明细 (`_剪辑明细.csv`)

- **格式**: CSV (Excel 可读)
- **内容**:
  - 视频信息汇总
  - 每个问题点的详细记录
  - 时间戳、类型、建议、时长

---

## 🔍 检测类型

### 语气词 (filler)

检测常见的语气词和填充词：
- 嗯、啊、这个、那个
- 然后、就是、好、可以
- 来去、对不对

### 过短片段 (too_short)

检测时长 < 0.5 秒 且内容 ≤ 3 字的片段

### 重复内容 (duplicate)

检测与前一片段完全相同的内容

---

## 💡 使用技巧

### 1. 调整字幕样式

编辑 `embed_subtitles()` 函数中的 FFmpeg 命令：

```python
force_style='FontName=Microsoft YaHei,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=1,Align=2'
```

参数：
- `FontName=Arial` - 改为英文字体
- `FontSize=36` - 增大字号
- `PrimaryColour=&H00FFFF` - 改为黄色

### 2. 自定义语气词列表

编辑 `analyze_content()` 函数：

```python
filler_words = ['嗯', '啊', '这个', '那个', '然后', '就是', '好', '可以', '来去', '对不对', '你的自定义词']
```

### 3. 提高识别准确率

使用更大的 Whisper 模型：

```python
WHISPER_MODEL = "medium"  # 或 "large"
```

---

## ⚠️ 常见问题

### Q: 字幕无法嵌入？

**A**: 检查以下几点：
1. FFmpeg 是否正确安装
2. 从技能目录执行脚本
3. 字幕文件编码为 UTF-8

### Q: Whisper 识别太慢？

**A**: 使用更小的模型：
```python
WHISPER_MODEL = "tiny"  # 最快但准确率较低
```

### Q: 检测不到语气词？

**A**: 
1. 检查语气词列表是否包含目标词
2. 查看字幕文件确认识别正确
3. 可能是字幕分段问题

### Q: 如何批量处理多个视频？

**A**: 修改主流程添加循环：

```python
for video_file in INPUT_DIR.glob("*.mov"):
    VIDEO_NAME = video_file.stem
    main()
```

---

## 📈 性能参考

### Whisper 模型性能

| 模型 | 10 分钟视频 | 准确率 |
|------|-----------|--------|
| tiny | ~1 分钟 | ⭐⭐ |
| base | ~2 分钟 | ⭐⭐⭐ |
| small | ~5 分钟 | ⭐⭐⭐⭐ |
| medium | ~10 分钟 | ⭐⭐⭐⭐⭐ |
| large | ~20 分钟 | ⭐⭐⭐⭐⭐ |

### FFmpeg 处理速度

- **嵌入字幕**: 约 1-2 倍实时速度
- **重新编码**: 约 0.5-1 倍实时速度

---

## 🎯 最佳实践

1. ✅ **备份原片** - 处理前保留原始文件
2. ✅ **人工审核** - AI 建议仅供参考
3. ✅ **测试小样** - 先用短视频测试配置
4. ✅ **定期检查** - 查看输出文件质量

---

## 📝 更新日志

### v3.0 (2026-03-24)
- ✅ 修复字幕嵌入问题
- ✅ 生成详细 CSV 报告
- ✅ 优化语义分析算法
- ✅ 简化代码提高可靠性

---

## 📚 相关资源

- [FFmpeg 文档](https://ffmpeg.org/documentation.html)
- [Whisper GitHub](https://github.com/openai/whisper)
- [SRT 字幕格式](https://en.wikipedia.org/wiki/SubRip)

---

*Video Smart Editor v3.0 - 让视频剪辑更智能*
