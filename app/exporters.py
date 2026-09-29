from fpdf import FPDF

from .config import BASE_DIR, EXPORTS_DIR


def _safe_text(value: str) -> str:

    return (
        value
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def save_pdf(comic) -> str:

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=12
    )

    for panel in comic.panels:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.cell(
            0,
            12,
            _safe_text(
                f"{comic.title} - Panel "
                f"{panel.panel_number}"
            ),
            ln=True
        )

        image_file = (
            BASE_DIR /
            panel.image_url.lstrip("/")
        )

        if image_file.exists():

            pdf.image(
                str(image_file),
                x=15,
                y=30,
                w=180
            )

        pdf.ln(115)

        pdf.set_font(
            "Helvetica",
            "B",
            12
        )

        pdf.multi_cell(
            0,
            8,
            _safe_text(
                "Scene: " + panel.scene
            )
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                "Narration: " +
                panel.narration
            )
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                "Dialogue: " +
                panel.dialogue
            )
        )

    filename = "comiccraft_comic.pdf"

    output = EXPORTS_DIR / filename

    pdf.output(str(output))

    return (
        "/static/exports/"
        + filename
    )