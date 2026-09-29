from fastapi import APIRouter, Request
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)
from fastapi.templating import Jinja2Templates

from .schemas import (
    ComicRequest,
    ComicResponse,
    Panel,
)

from .gemini_client import (
    generate_outline,
    generate_comic,
)

from .image_generator import (
    generate_image,
)

from .exporters import (
    save_pdf,
)

from .layout_builder import (
    build_comic_layout,
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "/",
    include_in_schema=False
)
async def home():

    return RedirectResponse(
        url="/create"
    )


@router.get("/health")
async def health():

    return {
        "status": "ok",
        "project": "ComicCraft"
    }


@router.get(
    "/create",
    response_class=HTMLResponse
)
async def create_page(
    request: Request
):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate_page(
    request: Request
):

    form = await request.form()

    data = ComicRequest(

        prompt=str(
            form.get(
                "prompt",
                ""
            )
        ),

        character_name=str(
            form.get(
                "character_name",
                ""
            )
        ),

        setting=str(
            form.get(
                "setting",
                ""
            )
        ),

        tone=str(
            form.get(
                "tone",
                "adventure"
            )
        ),

        art_style=str(
            form.get(
                "art_style",
                "comic book"
            )
        ),
    )

    # STEP 1:
    # Generate story outline

    outline = generate_outline(
        data
    )

    # STEP 2:
    # Generate five-panel comic

    raw_comic = generate_comic(
        data,
        outline
    )

    panels = []

    # STEP 3:
    # Generate images

    for raw_panel in raw_comic["panels"]:

        image_url = generate_image(

            raw_panel[
                "panel_number"
            ],

            raw_panel[
                "image_prompt"
            ],
        )

        panels.append(

            Panel(

                panel_number=
                    raw_panel[
                        "panel_number"
                    ],

                scene=
                    raw_panel[
                        "scene"
                    ],

                narration=
                    raw_panel[
                        "narration"
                    ],

                dialogue=
                    raw_panel[
                        "dialogue"
                    ],

                image_prompt=
                    raw_panel[
                        "image_prompt"
                    ],

                image_url=image_url,
            )
        )

    # STEP 4:
    # Create final response

    comic = ComicResponse(

        title=
            raw_comic["title"],

        outline=
            raw_comic.get(
                "outline",
                outline
            ),

        panels=panels,
    )

    # STEP 5:
    # Build layout

    layout = build_comic_layout(
        comic
    )

    # STEP 6:
    # Display comic

    return templates.TemplateResponse(

        "comic_preview.html",

        {
            "request": request,

            "comic": comic,

            "layout": layout,
        }
    )


@router.post(
    "/generate-comic/json"
)
async def generate_json(
    data: ComicRequest
):

    outline = generate_outline(
        data
    )

    raw_comic = generate_comic(
        data,
        outline
    )

    panels = []

    for raw_panel in raw_comic["panels"]:

        image_url = generate_image(

            raw_panel[
                "panel_number"
            ],

            raw_panel[
                "image_prompt"
            ],
        )

        panels.append(

            Panel(

                panel_number=
                    raw_panel[
                        "panel_number"
                    ],

                scene=
                    raw_panel[
                        "scene"
                    ],

                narration=
                    raw_panel[
                        "narration"
                    ],

                dialogue=
                    raw_panel[
                        "dialogue"
                    ],

                image_prompt=
                    raw_panel[
                        "image_prompt"
                    ],

                image_url=image_url,
            )
        )

    return ComicResponse(

        title=
            raw_comic["title"],

        outline=
            raw_comic.get(
                "outline",
                outline
            ),

        panels=panels,
    )


@router.post("/export")
async def export_comic(
    comic: ComicResponse
):

    pdf_url = save_pdf(
        comic
    )

    filename = (
        pdf_url.split("/")[-1]
    )

    return {

        "success": True,

        "filename": filename,

        "download_url": pdf_url,
    }


@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(
    request: Request
):

    return templates.TemplateResponse(

        "export_success.html",

        {
            "request": request,

            "filename":
                "comiccraft_comic.pdf",
        }
    )