---
name: video_smart_editor
description: 视频智能剪辑工具 - 基于语义理解的自动化视频剪辑，支持语音转录、字幕嵌入、语气词检测、剪辑建议生成
homepage: https://github.com/openclaw/openclaw
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["ffmpeg", "ffprobe", "whisper"], "python": true }, "env": [] } }
---

# Video Smart Editor - 视频智能剪辑技能

基于语义理解的自动化视频剪辑工具，支持语音转录、字幕嵌入、语气词检测、剪辑建议生成。

**版本**: v3.0  
**作者**: ClawX  
**许可证**: MIT

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

## 🚀 快速开始

### 基础用法

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\video_smart_editor
uv run python scripts/video_editor.py
```

### 配置说明

编辑脚本顶部的配置区域：

```python
INPUT_DIR = Path(r"E:\video_input")      # 输入目录
VIDEO_NAME = "日报助手"                   # 视频文件名（不含扩展名）
WHISPER_MODEL = "base"                   # Whisper 模型：tiny/base/small/medium/large
WHISPER_LANGUAGE = "zh"                  # 语言：zh/en/ja 等
```

---

## 📋 处理流程

### 阶段 1: 嵌入字幕 📜

1. **音频提取** - 从视频提取音轨
2. **Whisper 转录** - 生成带时间戳的 SRT 字幕
3. **字幕嵌入** - 使用 FFmpeg 将字幕硬编码到视频

### 阶段 2: 语义分析 🧠

1. **语气词检测** - 识别"嗯"、"啊"、"这个"、"就是"等
2. **过短片段检测** - 标记<0.5 秒的片段
3. **重复内容检测** - 发现重复语句

### 阶段 3: 生成报告 📊

1. **审稿报告** - Markdown 格式，包含问题列表和优化建议
2. **剪辑明细** - CSV 格式，详细记录每个问题点

---

## 📁 输出文件

| 文件 | 说明 | 格式 |
|------|------|------|
| `{视频名}_精简版.mp4` | 嵌入字幕的视频 | MP4 (H.264 + AAC) |
| `{视频名}_字幕.srt` | SRT 字幕文件 | SRT |
| `{视频名}_审稿报告.md` | 语义分析报告 | Markdown |
| `{视频名}_剪辑明细.csv` | 剪辑点详细记录 | CSV (Excel 可读) |

---

## 🔧 技术细节

### 字幕样式配置

在 `embed_subtitles()` 函数中修改：

```python
force_style='FontName=Microsoft YaHei,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=1,Align=2'
```

参数说明：
- `FontName`: 字体（默认微软雅黑）
- `FontSize`: 字号（默认 24）
- `PrimaryColour`: 主颜色（白色）
- `OutlineColour`: 描边颜色（黑色）
- `Outline`: 描边宽度（1）
- `Align`: 对齐方式（2=底部居中）

### 语气词检测列表

在 `analyze_content()` 函数中修改：

```python
filler_words = ['嗯', '啊', '这个', '那个', '然后', '就是', '好', '可以', '来去', '对不对']
```

---

## 📊 输出示例

### 审稿报告（Markdown）

```markdown
# 视频语义审稿报告

## 📊 基本信息
- 总片段数：154
- 视频时长：278.6 秒
- 发现问题：7 处

## ⚠️ 发现的问题
- [00:01:43,000] filler: 这个 → 建议：删除语气词
- [00:01:58,000] filler: 就是 → 建议：删除语气词

## 💡 优化建议
1. 删除语气词使内容更专业
2. 移除过短片段提升流畅度
```

### 剪辑明细（CSV）

```csv
视频信息,,,
原始视频，日报助手.mov,,
输出视频，日报助手_精简版.mp4,,
视频时长，278.62 秒,,
字幕片段，154 个,,
发现问题，7 处,,

序号，类型，时间，内容，建议，时长 (秒)
1,filler,00:01:43,000,"这个",删除语气词，1.00
2,filler,00:01:58,000,"就是",删除语气词，1.00
```

---

## ⚙️ 依赖安装

### 系统依赖

```bash
# Windows
ffmpeg -version  # 检查是否安装
```

如未安装，从 https://ffmpeg.org/download.html 下载

### Python 依赖

```bash
uv pip install openai-whisper
```

---

## 🔍 常见问题

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

### Q: 想检测更多语气词？

**A**: 编辑 `filler_words` 列表添加你的自定义词

### Q: 如何实际剪辑掉语气词？

**A**: 当前版本生成剪辑建议，实际剪辑需要：
1. 使用专业剪辑软件导入 CSV
2. 或开发 v4.0 版本实现自动剪辑

---

## 📈 性能优化

### Whisper 模型选择

| 模型 | 速度 | 准确率 | 推荐场景 |
|------|------|--------|----------|
| tiny | ⚡⚡⚡ | ⭐⭐ | 快速测试 |
| base | ⚡⚡ | ⭐⭐⭐ | 日常使用 ✅ |
| small | ⚡ | ⭐⭐⭐⭐ | 高质量需求 |
| medium | 🐌 | ⭐⭐⭐⭐⭐ | 专业场景 |
| large | 🐌🐌 | ⭐⭐⭐⭐⭐ | 极致质量 |

### FFmpeg 参数调优

```python
# 更快编码（文件更大）
-c:v libx264 -preset fast -crf 23

# 更小文件（编码更慢）
-c:v libx264 -preset slow -crf 28
```

---

## 🎯 最佳实践

1. **视频命名** - 使用简洁的中文名，避免特殊字符
2. **目录结构** - 输入输出分开管理
3. **备份原片** - 剪辑前保留原始文件
4. **人工审核** - AI 建议仅供参考，最终剪辑需人工确认

---

## 📝 更新日志

### v3.0 (2026-03-24)
- ✅ 修复字幕嵌入问题
- ✅ 生成详细 CSV 报告
- ✅ 优化语义分析算法
- ✅ 简化代码提高可靠性

### v2.0 (2026-03-24)
- ⚠️ 尝试自动剪辑但 FFmpeg 滤镜过于复杂

### v1.0 (2026-03-23)
- 🎉 初始版本
- 基础语音转录
- 简单语义分析

---

## 📚 相关技能

- **video_auto_cut** - 基于场景检测的视频自动剪辑
- **video_auto_narrator** - 视频自动解说配音
- **video_auto_remix** - 爆款视频复刻

---

## 💬 技术支持

遇到问题？检查以下事项：

1. FFmpeg 是否在 PATH 中
2. Python 环境是否正确
3. 输入文件路径是否正确
4. 查看错误日志详细信息

---

*Video Smart Editor v3.0 - 让视频剪辑更智能*
