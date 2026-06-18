# ViralForge Skill

> AI视频生成 + 社交媒体自动发布 — 本地 SVD + DeepSeek V4 Pro

## 能力

ViralForge 是一个 AI 视频营销自动化 Skill，通过 LangGraph 8节点流水线实现：

1. **视频生成** — 文本转视频 / 图片转视频，支持 ComfyUI+SVD 本地或 DeepSeek V4 Pro 远程
2. **SEO 优化** — 自动生成标题、标签、描述，关键词趋势分析
3. **一键发布** — 同时分发到 Facebook / YouTube / Twitter / LinkedIn / Instagram / TikTok
4. **学习优化** — 持续分析数据，自动调整发布策略

## 安装

```
codex skill add auauhack-prog/-viralforgeseo
```

或

```
npx skills add auauhack-prog/-viralforgeseo
```

## Quick Start

```bash
git clone https://github.com/auauhack-prog/-viralforgeseo.git
cd viralforge
pip install -r requirements.txt
cp .env.example .env
```

编辑 `.env` 配置各平台 API Token，然后运行 `./启动.command`。

## 技术栈

- LangGraph (8节点状态机)
- ComfyUI + Stable Video Diffusion (本地视频生成)
- DeepSeek V4 Pro API (远程高级生成)
- 6大社交媒体 API (FB/YT/TW/LI/IG/TK)
- Python 3.11+ (pydantic, requests, opencv, moviepy)

## 演示

https://skill.600.im
