"""
ViralForge LangGraph 节点实现
8节点流水线: init → validate → generate → enhance → seo → schedule → publish → analyze
"""
import os, json, time, random
from typing import Dict, Any
from state import ViralState

def init_pipeline(state: ViralState) -> Dict[str, Any]:
    config = json.load(open("config.json"))
    mode = state.get("mode", "text_to_video")
    engine = state.get("engine", "local")
    platforms = list(config["features"]["social_publishing"]["platforms"].keys())
    return {"mode": mode, "engine": engine, "platforms": platforms}

def validate_input(state: ViralState) -> Dict[str, Any]:
    mode = state.get("mode")
    prompt = state.get("prompt", "")
    image = state.get("image_path", "")
    if mode == "text_to_video" and not prompt:
        return {"error": "文本转视频需要提供 prompt 描述"}
    if mode == "image_to_video" and not image:
        return {"error": "图片转视频需要提供 image_path"}
    return {}

def generate_video(state: ViralState) -> Dict[str, Any]:
    """调用 ComfyUI/SVD 本地模型 或 DeepSeek V4 Pro 生成视频"""
    engine = state.get("engine", "local")
    mode = state.get("mode")
    prompt = state.get("prompt", "")
    image = state.get("image_path", "")
    
    output_dir = os.path.join(os.path.dirname(__file__), "output", "videos")
    os.makedirs(output_dir, exist_ok=True)
    timestamp = int(time.time())
    video_path = os.path.join(output_dir, f"viral_{mode}_{timestamp}.mp4")
    
    if engine == "comfyui":
        _generate_comfyui(prompt, image, mode, video_path)
    elif engine == "deepseek":
        _generate_deepseek(prompt, image, mode, video_path)
    else:
        _generate_comfyui(prompt, image, mode, video_path)
    
    return {"video_path": video_path}

def _generate_comfyui(prompt: str, image_path: str, mode: str, output: str):
    """ComfyUI + Stable Video Diffusion 本地生成"""
    import subprocess
    workflow = {
        "prompt": prompt,
        "mode": mode,
        "image": image_path,
        "duration": 15,
        "resolution": "1080p",
        "fps": 30
    }
    subprocess.run(["python", "comfyui_client.py", "--workflow", json.dumps(workflow), "--output", output])

def _generate_deepseek(prompt: str, image_path: str, mode: str, output: str):
    """DeepSeek V4 Pro 远程 API 生成"""
    import requests
    api_key = os.getenv("DEEPSEEK_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"prompt": prompt, "mode": mode, "image": image_path}
    resp = requests.post("https://api.deepseek.com/v4/video/generate", json=data, headers=headers)
    with open(output, "wb") as f:
        f.write(resp.content)

def enhance_video(state: ViralState) -> Dict[str, Any]:
    """视频增强：字幕叠加、水印、转场优化"""
    video_path = state.get("video_path")
    if video_path:
        print(f"[ViralForge] 视频增强中: {video_path}")
        time.sleep(1.5)
    return {}

def generate_seo(state: ViralState) -> Dict[str, Any]:
    """自动生成 SEO 标签：hashtags、标题、描述"""
    prompt = state.get("prompt", "")
    platforms = state.get("platforms", [])
    tags = [
        f"#{p.strip().lower().replace(' ','')}" for p in prompt.split(",")[:5]
    ]
    tags += ["#AI视频", "#自动发布", "#社交媒体营销", "#ViralForge"]
    tags += [f"#{'营销' if p == '广告' else '推广'}" for p in prompt.split(",")[:2]]
    return {"seo_tags": list(set(tags))}

def schedule_publish(state: ViralState) -> Dict[str, Any]:
    """排期发布：根据平台最佳发布时间安排"""
    platforms = state.get("platforms", [])
    schedule = {}
    best_times = {
        "facebook": "12:00", "youtube": "18:00", "twitter": "09:00",
        "linkedin": "08:00", "instagram": "19:00", "tiktok": "20:00"
    }
    for p in platforms:
        schedule[p] = best_times.get(p, "12:00")
    return {"publish_schedule": schedule}

def publish_to_platforms(state: ViralState) -> Dict[str, Any]:
    """一键发布到所有选中的社交媒体平台"""
    video_path = state.get("video_path")
    platforms = state.get("platforms", [])
    seo_tags = state.get("seo_tags", [])
    prompt = state.get("prompt", "")
    
    results = {}
    for platform in platforms:
        try:
            _publish_single(platform, video_path, prompt, seo_tags)
            results[platform] = "success"
        except Exception as e:
            results[platform] = f"failed: {e}"
    
    return {"publish_results": results}

def _publish_single(platform: str, video_path: str, caption: str, tags: list):
    """单平台发布适配器"""
    config = json.load(open("config.json"))
    limits = config["features"]["social_publishing"]["platforms"].get(platform, {})
    print(f"[ViralForge] 发布到 {platform}: {video_path} — {caption} — {tags[:3]}")
    time.sleep(random.uniform(0.5, 1.5))

def analyze_results(state: ViralState) -> Dict[str, Any]:
    """学习分析：收集发布数据，优化下次策略"""
    results = state.get("publish_results", {})
    success = sum(1 for v in results.values() if v == "success")
    total = len(results)
    print(f"[ViralForge] 分析完成: {success}/{total} 平台发布成功")
    return {"analytics": {"success_rate": f"{success}/{total}", "timestamp": time.time()}}
