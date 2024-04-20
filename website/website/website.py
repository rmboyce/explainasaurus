"""The main Chat app."""

import reflex as rx
from website.components import navbar, pdf


def index() -> rx.Component:
    """The main app."""
    return rx.chakra.vstack(
        navbar(),
        pdf.pdf_upload(),
        background_color=rx.color("mauve", 12),
        color=rx.color("mauve", 1),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )


# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="indigo",
    ),
)
app.add_page(index)
