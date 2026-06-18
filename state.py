"""ViralForge 状态定义"""
from typing import TypedDict, Optional, Dict, List

class ViralState(TypedDict):
    prompt: str
    image_path: Optional[str]
    mode: str
    engine: str
    video_path: Optional[str]
    platforms: List[str]
    seo_tags: List[str]
    publish_schedule: Dict[str, str]
    publish_results: Dict[str, str]
    analytics: Dict[str, str]
    error: Optional[str]
