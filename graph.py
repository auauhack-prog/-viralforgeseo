"""
ViralForge - AI Video Generation & Social Media Auto-Publishing
LangGraph StateGraph 入口：8节点视频生成+发布流水线
"""
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

class ViralState(TypedDict):
    prompt: str
    image_path: Optional[str]
    mode: str  # "text_to_video" | "image_to_video"
    engine: str  # "local" | "deepseek"
    video_path: Optional[str]
    platforms: list[str]
    seo_tags: list[str]
    publish_results: dict
    analytics: dict
    error: Optional[str]

from nodes import (
    init_pipeline, validate_input, generate_video,
    enhance_video, generate_seo, schedule_publish,
    publish_to_platforms, analyze_results
)

def build_graph():
    workflow = StateGraph(ViralState)
    
    workflow.add_node("init", init_pipeline)
    workflow.add_node("validate", validate_input)
    workflow.add_node("generate", generate_video)
    workflow.add_node("enhance", enhance_video)
    workflow.add_node("seo", generate_seo)
    workflow.add_node("schedule", schedule_publish)
    workflow.add_node("publish", publish_to_platforms)
    workflow.add_node("analyze", analyze_results)
    
    workflow.set_entry_point("init")
    workflow.add_edge("init", "validate")
    workflow.add_conditional_edges("validate", lambda s: "error" if s.get("error") else "generate",
                                    {"generate": "generate", "error": "analyze"})
    workflow.add_edge("generate", "enhance")
    workflow.add_edge("enhance", "seo")
    workflow.add_edge("seo", "schedule")
    workflow.add_edge("schedule", "publish")
    workflow.add_edge("publish", "analyze")
    workflow.add_edge("analyze", END)
    
    return workflow.compile()

if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"prompt": "产品宣传视频", "mode": "text_to_video", "engine": "local"})
    print(result)
