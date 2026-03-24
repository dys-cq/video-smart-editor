#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Video Smart Editor v3.0 - 简化可靠版
1. 嵌入字幕到视频
2. 生成详细剪辑报告
3. 使用简单可靠的 FFmpeg 命令
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import re

# ==================== 配置 ====================

INPUT_DIR = Path(r"E:\video_input")
OUTPUT_DIR = INPUT_DIR / "output"
WORK_DIR = INPUT_DIR / "work"

OUTPUT_DIR.mkdir(exist_ok=True)
WORK_DIR.mkdir(exist_ok=True)

VIDEO_NAME = "日报助手"
INPUT_VIDEO = INPUT_DIR / f"{VIDEO_NAME}.mov"

# ==================== 工具函数 ====================

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def time_to_seconds(time_str):
    match = re.match(r'(\d{2}):(\d{2}):(\d{2})[,\.](\d{3})', time_str)
    if not match:
        return 0
    h, m, s, ms = map(int, match.groups())
    return h * 3600 + m * 60 + s + ms / 1000

def parse_srt(srt_path):
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\n*$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    subtitles = []
    for match in matches:
        index, start, end, text = match
        subtitles.append({
            'index': int(index),
            'start': start,
            'end': end,
            'start_sec': time_to_seconds(start),
            'end_sec': time_to_seconds(end),
            'text': text.strip().replace('\n', ' ')
        })
    
    return subtitles

# ==================== 阶段 1: 嵌入字幕 ====================

def embed_subtitles():
    """将字幕嵌入视频"""
    log("=" * 60)
    log("阶段 1: 嵌入字幕到视频")
    log("=" * 60)
    
    srt_path = OUTPUT_DIR / f"{VIDEO_NAME}_字幕.srt"
    output_video = OUTPUT_DIR / f"{VIDEO_NAME}_精简版.mp4"
    
    if not srt_path.exists():
        log(f"❌ 字幕文件不存在：{srt_path}")
        return False
    
    # 切换到 work 目录使用相对路径
    original_cwd = os.getcwd()
    os.chdir(str(WORK_DIR))
    
    try:
        srt_rel = f"../output/{VIDEO_NAME}_字幕.srt"
        output_rel = f"../output/{VIDEO_NAME}_精简版.mp4"
        input_rel = f"../{VIDEO_NAME}.mov"
        
        # 简单的 FFmpeg 命令：添加硬字幕
        cmd = f'ffmpeg -y -i "{input_rel}" -vf "subtitles={srt_rel}:force_style=\'FontName=Microsoft YaHei,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=1,Align=2\'" -c:a copy "{output_rel}"'
        
        log(f"执行 FFmpeg 命令...")
        log(f"输入：{input_rel}")
        log(f"字幕：{srt_rel}")
        log(f"输出：{output_rel}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        # 检查是否成功
        if 'video:' in result.stderr and 'audio:' in result.stderr:
            log(f"✅ 字幕嵌入成功")
            
            if output_video.exists():
                size_mb = output_video.stat().st_size / 1024 / 1024
                log(f"输出文件：{output_video} ({size_mb:.1f} MB)")
                
                # 获取视频时长
                cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{output_video}"'
                dur_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                duration = float(dur_result.stdout.strip())
                log(f"视频时长：{duration:.2f}秒")
                
                os.chdir(original_cwd)
                return True, duration
        else:
            log(f"❌ FFmpeg 失败")
            log(f"错误：{result.stderr[:500]}")
            os.chdir(original_cwd)
            return False, 0
            
    except Exception as e:
        log(f"❌ 异常：{e}")
        os.chdir(original_cwd)
        return False, 0

# ==================== 阶段 2: 语义分析 ====================

def analyze_content(subtitles):
    """分析字幕内容，标记可优化点"""
    log("=" * 60)
    log("阶段 2: 语义分析")
    log("=" * 60)
    
    filler_words = ['嗯', '啊', '这个', '那个', '然后', '就是', '好', '可以', '来去', '对不对']
    
    issues = []
    for i, sub in enumerate(subtitles):
        text = sub['text']
        duration = sub['end_sec'] - sub['start_sec']
        
        # 检测语气词
        for filler in filler_words:
            if text == filler or text.strip() == filler:
                issues.append({
                    'type': 'filler',
                    'segment': i,
                    'time': sub['start'],
                    'end_time': sub['end'],
                    'text': text,
                    'duration': duration,
                    'suggestion': '删除语气词'
                })
                break
        
        # 检测过短片段
        if duration < 0.5 and len(text) <= 3 and text not in filler_words:
            issues.append({
                'type': 'too_short',
                'segment': i,
                'time': sub['start'],
                'end_time': sub['end'],
                'text': text,
                'duration': duration,
                'suggestion': '过短片段'
            })
    
    log(f"发现 {len(issues)} 个可优化点")
    return issues

def generate_reports(subtitles, issues, video_duration):
    """生成审稿报告和剪辑明细 CSV"""
    log("=" * 60)
    log("阶段 3: 生成报告")
    log("=" * 60)
    
    # 1. 审稿报告
    report_path = OUTPUT_DIR / f"{VIDEO_NAME}_审稿报告.md"
    
    report = f"""# 视频语义审稿报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**源文件**: {INPUT_VIDEO}

## 📊 基本信息

- **总片段数**: {len(subtitles)}
- **视频时长**: {video_duration:.1f}秒
- **发现问题**: {len(issues)} 处

## ⚠️ 发现的问题

"""
    
    for issue in issues[:30]:
        report += f"- **[{issue['time']}]** {issue['type']}: {issue['text']}\n"
        report += f"  → 建议：{issue['suggestion']}\n\n"
    
    report += f"""## 💡 优化建议

1. 删除语气词使内容更专业
2. 移除过短片段提升流畅度
3. 可考虑重新录制问题片段

---
*Video Smart Editor v3.0*
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    log(f"审稿报告：{report_path}")
    
    # 2. 剪辑明细 CSV
    csv_path = OUTPUT_DIR / f"{VIDEO_NAME}_剪辑明细.csv"
    
    with open(csv_path, 'w', encoding='utf-8-sig') as f:
        f.write("视频信息,,,\n")
        f.write(f"原始视频，{INPUT_VIDEO.name},,\n")
        f.write(f"输出视频，{VIDEO_NAME}_精简版.mp4,,\n")
        f.write(f"视频时长，{video_duration:.2f}秒,,\n")
        f.write(f"字幕片段，{len(subtitles)}个,,\n")
        f.write(f"发现问题，{len(issues)}处,,\n")
        f.write(f"\n")
        f.write(f"序号，类型，时间，内容，建议，时长 (秒)\n")
        
        for i, issue in enumerate(issues, 1):
            text = issue['text'].replace('"', '""').replace(',', '，')
            f.write(f"{i},{issue['type']},{issue['time']},\"{text}\",{issue['suggestion']},{issue['duration']:.2f}\n")
    
    log(f"剪辑明细：{csv_path}")
    log(f"共 {len(issues)} 条记录")
    
    return True

# ==================== 主流程 ====================

def main():
    log("=" * 60)
    log("Video Smart Editor v3.0 - 视频智能剪辑")
    log("=" * 60)
    log(f"输入视频：{INPUT_VIDEO}")
    log(f"输出目录：{OUTPUT_DIR}")
    log("=" * 60)
    
    if not INPUT_VIDEO.exists():
        log(f"❌ 错误：找不到输入文件 {INPUT_VIDEO}")
        return False
    
    # 阶段 1: 嵌入字幕
    success, video_duration = embed_subtitles()
    if not success:
        log("❌ 阶段 1 失败")
        return False
    
    # 读取字幕进行分析
    srt_path = OUTPUT_DIR / f"{VIDEO_NAME}_字幕.srt"
    subtitles = parse_srt(srt_path)
    log(f"解析到 {len(subtitles)} 个字幕片段")
    
    # 阶段 2: 语义分析
    issues = analyze_content(subtitles)
    
    # 阶段 3: 生成报告
    generate_reports(subtitles, issues, video_duration)
    
    # 完成
    log("=" * 60)
    log("🎉 全部完成！")
    log("=" * 60)
    log(f"输出文件:")
    log(f"  1. {OUTPUT_DIR / f'{VIDEO_NAME}_精简版.mp4'} ({video_duration:.1f}秒) - **已嵌入字幕**")
    log(f"  2. {OUTPUT_DIR / f'{VIDEO_NAME}_字幕.srt'} ({len(subtitles)}个片段)")
    log(f"  3. {OUTPUT_DIR / f'{VIDEO_NAME}_审稿报告.md'} ({len(issues)}个问题)")
    log(f"  4. {OUTPUT_DIR / f'{VIDEO_NAME}_剪辑明细.csv'} ({len(issues)}条记录)")
    log("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"❌ 异常：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
