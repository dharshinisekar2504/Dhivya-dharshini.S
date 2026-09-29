# ComicCraft - AI Comic Story Creator

ComicCraft is an AI-powered web application that creates comic stories from user prompts.

## Technologies

- Python
- FastAPI
- Gemini
- Stable Diffusion
- Jinja2
- HTML
- CSS
- PDF generation

## Installation

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1

Install packages:

pip install -r requirements.txt

Create a .env file from .env.example.

Add your Gemini API key.

Keep:

IMAGE_PROVIDER=placeholder

Run:

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/create

## Optional Stable Diffusion

Install:

pip install -r requirements-ai.txt

Then change:

IMAGE_PROVIDER=diffusers

Restart the application.

## Project Flow

User Input

↓

Gemini Story Outline

↓

Gemini Five Comic Panels

↓

Image Generation

↓

Comic Preview

↓

PDF Export