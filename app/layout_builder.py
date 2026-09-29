def build_comic_layout(comic):

    return {
        "title": comic.title,

        "outline": comic.outline,

        "panels": [

            {
                "number": panel.panel_number,

                "scene": panel.scene,

                "narration": panel.narration,

                "dialogue": panel.dialogue,

                "image_url": panel.image_url,
            }

            for panel in comic.panels
        ],
    }