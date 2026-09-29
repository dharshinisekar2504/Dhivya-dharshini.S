from typing import List
from pydantic import BaseModel, Field


class ComicRequest(BaseModel):
    prompt: str = Field(..., min_length=3)
    character_name: str = Field(..., min_length=1)
    setting: str = Field(..., min_length=1)
    tone: str = Field(default="adventure")
    art_style: str = Field(default="comic book")


class Panel(BaseModel):
    panel_number: int
    scene: str
    narration: str
    dialogue: str
    image_prompt: str
    image_url: str = ""


class ComicResponse(BaseModel):
    title: str
    outline: str
    panels: List[Panel]