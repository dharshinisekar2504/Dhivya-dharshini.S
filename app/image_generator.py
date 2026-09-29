from PIL import Image, ImageDraw

from .config import (
    IMAGE_PROVIDER,
    IMAGE_MODEL,
    IMAGE_STEPS,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    PANELS_DIR,
)


_pipeline = None


def _placeholder(panel_number: int, prompt: str) -> str:

    path = PANELS_DIR / f"panel_{panel_number}.png"

    image = Image.new(
        "RGB",
        (IMAGE_WIDTH, IMAGE_HEIGHT),
        "white"
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (
            10,
            10,
            IMAGE_WIDTH - 10,
            IMAGE_HEIGHT - 10
        ),
        outline="black",
        width=5
    )

    draw.text(
        (30, 30),
        f"ComicCraft - Panel {panel_number}",
        fill="black"
    )

    text = prompt[:500]

    y = 90

    for i in range(0, len(text), 55):

        line = text[i:i + 55]

        draw.text(
            (30, y),
            line,
            fill="black"
        )

        y += 24

        if y > IMAGE_HEIGHT - 40:
            break

    image.save(path)

    return f"/static/panels/{path.name}"


def _get_pipeline():

    global _pipeline

    if _pipeline is None:

        import torch

        from diffusers import StableDiffusionPipeline

        device = "cuda" if torch.cuda.is_available() else "cpu"

        _pipeline = StableDiffusionPipeline.from_pretrained(
            IMAGE_MODEL
        )

        _pipeline = _pipeline.to(device)

    return _pipeline


def generate_image(
    panel_number: int,
    prompt: str
) -> str:

    if IMAGE_PROVIDER == "placeholder":

        return _placeholder(
            panel_number,
            prompt
        )

    if IMAGE_PROVIDER != "diffusers":

        raise ValueError(
            "IMAGE_PROVIDER must be "
            "'placeholder' or 'diffusers'."
        )

    try:

        pipeline = _get_pipeline()

        image = pipeline(
            prompt,
            num_inference_steps=IMAGE_STEPS,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT,
        ).images[0]

        path = PANELS_DIR / f"panel_{panel_number}.png"

        image.save(path)

        return f"/static/panels/{path.name}"

    except Exception as exc:

        print(
            f"Image generation failed: {exc}"
        )

        print(
            "Using placeholder image instead."
        )

        return _placeholder(
            panel_number,
            prompt
        )