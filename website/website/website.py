"""The main Chat app."""

import reflex as rx
from website.components import navbar, pdf
from website.state import api_test

def index() -> rx.Component:
    """The main app."""
    return rx.chakra.vstack(
        navbar(),
        pdf.pdf_upload(),
        color_scheme="slate",
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
app.api.add_api_route("/add_expl/", api_test, methods=["POST"])
