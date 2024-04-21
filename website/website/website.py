"""The main Chat app."""

import reflex as rx
from website.components import navbar, pdf
from website.state import State, api_test

def index() -> rx.Component:
    """The main app."""
    return rx.chakra.vstack(
        navbar(),
        rx.cond(State.summary != "",
                rx.box(
                    rx.vstack(
                        rx.text("Summary", font_weight="bold"),
                        rx.text(State.summary),
                        padding="1.4em",
                        margin="3em",
                        border="1px dashed rgb(107,99,246)",
                    ),
                )),
        rx.cond(State.relativearticles != "",
                rx.box(
                    rx.vstack(
                        rx.text("Similar articles", font_weight="bold"),
                        rx.text(State.relativearticles),
                        padding="1.4em",
                        margin="3em",
                        border="1px dashed rgb(107,99,246)",
                    ),
                )),
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
