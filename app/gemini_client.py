import json

from google import genai
from google.genai import types

from .config import GEMINI_API_KEY, GEMINI_MODEL, MAX_PANELS


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Create a .env file and add your Gemini API key."
    )


client = genai.Client(api_key=GEMINI_API_KEY)


def _generate(prompt: str) -> str:

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            response_mime_type="text/plain",
        ),
    )

    return response.text.strip()


def generate_outline(data) -> str:

    prompt = f"""
Create a short comic story outline.

Story idea:
{data.prompt}

Main character:
{data.character_name}

Setting:
{data.setting}

Tone:
{data.tone}

Art style:
{data.art_style}

Give a clear beginning, middle, conflict and ending.

Keep the story suitable for a general audience.
"""

    return _generate(prompt)


def generate_comic(data, outline: str) -> dict:

    prompt = f"""
You are the story engine for ComicCraft,
an AI comic story creator.

Create exactly {MAX_PANELS} comic panels.

Story idea:
{data.prompt}

Main character:
{data.character_name}

Setting:
{data.setting}

Tone:
{data.tone}

Art style:
{data.art_style}

Outline:
{outline}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "title": "short comic title",
  "outline": "short outline",
  "panels": [
    {{
      "panel_number": 1,
      "scene": "what is happening visually",
      "narration": "short narration",
      "dialogue": "short dialogue",
      "image_prompt": "detailed visual prompt for an image generator"
    }}
  ]
}}

Rules:

1. Create exactly {MAX_PANELS} panels.
2. Keep narration short.
3. Keep dialogue short.
4. Make every image_prompt detailed.
5. Include characters, action, setting and lighting.
6. Follow the requested art style.
7. Do not include markdown.
"""

    raw = _generate(prompt)

    raw = raw.replace("```json", "")
    raw = raw.replace("```", "")
    raw = raw.strip()

    try:
        result = json.loads(raw)

    except json.JSONDecodeError:

        start = raw.find("{")
        end = raw.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "Gemini did not return valid JSON."
            )

        result = json.loads(
            raw[start:end + 1]
        )

    if "panels" not in result:
        raise ValueError(
            "Gemini response does not contain panels."
        )

    if len(result["panels"]) != MAX_PANELS:
        raise ValueError(
            "Gemini did not return exactly five comic panels."
        )

    return result