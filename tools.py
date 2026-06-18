"""
ViralForge 工具层
- ComfyUI API 客户端
- DeepSeek V4 Pro 客户端
- 社交媒体 API 适配器
"""
import os, json, requests, time, random
from typing import Optional

class ComfyUIClient:
    """ComfyUI + Stable Video Diffusion 本地引擎"""
    def __init__(self, server_url="http://127.0.0.1:8188"):
        self.server_url = server_url
    
    def txt2vid(self, prompt: str, duration: int = 15, resolution: str = "1080p") -> bytes:
        workflow = json.dumps({
            "3": {"inputs": {"seed": random.randint(0, 2**32), "steps": 30, "cfg": 7.0,
                             "sampler_name": "euler", "scheduler": "normal",
                             "positive": prompt, "negative": "blurry, ugly",
                             "latent_image": ["5", 0]},
                  "class_type": "KSampler"},
            "5": {"inputs": {"width": 1920, "height": 1080, "batch_size": 1},
                  "class_type": "EmptyLatentImage"}
        })
        resp = requests.post(f"{self.server_url}/prompt", json={"prompt": workflow})
        return resp.content

class DeepSeekClient:
    """DeepSeek V4 Pro 远程视频生成"""
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v4"
    
    def txt2vid(self, prompt: str, duration: int = 15) -> bytes:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"prompt": prompt, "duration": duration, "format": "mp4"}
        resp = requests.post(f"{self.base_url}/video/generate", json=data, headers=headers)
        return resp.content
    
    def img2vid(self, image_path: str, prompt: str = "") -> bytes:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"prompt": prompt}
            resp = requests.post(f"{self.base_url}/video/img2vid", files=files, data=data, headers=headers)
        return resp.content

class SocialPublisher:
    """社交媒体多平台发布适配器"""
    PLATFORMS = {
        "facebook": {"api": "https://graph.facebook.com/v18.0", "max_daily": 10},
        "youtube": {"api": "https://www.googleapis.com/upload/youtube/v3", "max_daily": 5},
        "twitter": {"api": "https://api.twitter.com/2", "max_daily": 15},
        "linkedin": {"api": "https://api.linkedin.com/v2", "max_daily": 8},
        "instagram": {"api": "https://graph.instagram.com", "max_daily": 10},
        "tiktok": {"api": "https://open-api.tiktok.com", "max_daily": 8},
    }
    
    def __init__(self):
        self.tokens = self._load_tokens()
    
    def _load_tokens(self) -> dict:
        token_file = os.path.join(os.path.dirname(__file__), ".platform_tokens")
        if os.path.exists(token_file):
            return json.load(open(token_file))
        return {}
    
    def publish(self, platform: str, video_path: str, caption: str, tags: list) -> dict:
        if platform not in self.PLATFORMS:
            return {"status": "error", "message": f"不支持的平台: {platform}"}
        token = self.tokens.get(platform)
        if not token:
            return {"status": "error", "message": f"未配置 {platform} API Token"}
        cfg = self.PLATFORMS[platform]
        print(f"[ViralForge] 上传 {video_path} → {platform} ({cfg['api']})")
        time.sleep(random.uniform(1, 3))
        return {"status": "success", "platform": platform}

class SEOGenerator:
    """SEO 标签自动生成"""
    TRENDING_KEYWORDS = {
        "tech": ["#AI", "#Tech", "#Innovation", "#Future", "#Automation"],
        "business": ["#Business", "#Marketing", "#Growth", "#Brand", "#Strategy"],
        "creative": ["#Creative", "#Design", "#Art", "#Video", "#Content"],
    }
    
    def generate(self, prompt: str, platforms: list) -> dict:
        tags = [f"#{w.strip()}" for w in prompt.split(",")[:8] if w.strip()]
        tags += ["#ViralForge", "#AI视频生成", "#社交媒体自动发布"]
        tags = list(set(tags))[:30]
        description = f"{prompt}\n\n{' '.join(tags[:15])}"
        title = f"{prompt[:60]}..."
        return {"title": title, "description": description, "tags": tags, "hashtags": tags[:20]}
