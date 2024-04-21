import reflex as rx
from website.state import State

def sidebar_chat(hist: str, index: int) -> rx.Component:
    """A sidebar chat item.

    Args:
        chat: The chat item.
    """
    return rx.cond(
        hist["checked"],
        rx.vstack(
            rx.hstack(rx.text("link:", font_weight="bold"), rx.text(hist["link"]),),
            rx.hstack(rx.text("text:", font_weight="bold"), rx.text(hist["selected"]),),
            rx.hstack(rx.text("explanation:", font_weight="bold"), rx.text(hist["response"]),),
            on_click=State.shistory_toggle_checked(index),
            background_color=rx.color("indigo", 4),
            border="2px solid black",
            border_radius="10px",
            padding="20px"
        ),
        rx.vstack(
            rx.hstack(rx.text("link:", font_weight="bold"), rx.text(hist["link"]),),
            rx.hstack(rx.text("text:", font_weight="bold"), rx.text(hist["selected"]),),
            rx.hstack(rx.text("explanation:", font_weight="bold"), rx.text(hist["response"]),),
            on_click=State.shistory_toggle_checked(index),
            border="2px solid black",
            border_radius="10px",
            padding="20px"
        )
    )


def sidebar(trigger) -> rx.Component:
    """The sidebar component."""
    return rx.drawer.root(
        rx.drawer.trigger(trigger),
        rx.drawer.overlay(),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.heading("History", color=rx.color("slate", 11)),
                    rx.divider(size="4"),
                    rx.hstack(
                        rx.drawer.close(
                            rx.button(
                                "find similar articles",
                                on_click=State.generate_relativearticles(),
                                disabled=State.shistory_none_checked
                            ),
                            float="left"
                        ),
                        rx.drawer.close(
                            rx.button(
                                "generate summary",
                                on_click=State.generate_summary(),
                                disabled=State.shistory_none_checked
                            ),
                            float="right"
                        ),
                        width="100%",
                        display="block"
                    ),
                    rx.foreach(State.shistory, lambda hist, index: sidebar_chat(hist, index)),
                    align_items="stretch",
                    width="100%",
                    overflow_y="auto"
                ),
                top="auto",
                right="auto",
                height="100%",
                width="90%",
                padding="2em",
                background_color=rx.color("slate", 2),
                outline="none",
            )
        ),
        direction="left",
    )


def modal(trigger) -> rx.Component:
    """A modal to create a new chat."""
    return rx.dialog.root(
        rx.dialog.trigger(trigger),
        rx.dialog.content(
            rx.hstack(
                rx.input(
                    placeholder="Type something...",
                    on_blur=State.set_new_chat_name,
                    width=["15em", "20em", "30em", "30em", "30em", "30em"],
                ),
                rx.dialog.close(
                    rx.button(
                        "Create chat",
                        on_click=State.create_chat,
                    ),
                ),
                background_color=rx.color("slate", 1),
                spacing="2",
                width="100%",
            ),
        ),
    )


def navbar():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.button(
                    rx.hstack( 
                        rx.image(src="/dino.png",width="50px", height="50px", border_radius="50%"),
                        rx.heading(
                            "Explainasaurus",
                            color=rx.color("indigo", 1),
                        ),
                        align_items="center",
                    ),
                    on_click=State.set_uploaded(False),
                    background_color=rx.color("slate", 10)
                ),
                align_items="center",
            ),
            rx.hstack(
                sidebar(
                    rx.button(
                        rx.icon(
                            tag="history",
                        ),
                        on_click=State.set_hist(),
                    )
                ),
                rx.color_mode.button(
                    rx.color_mode.icon()
                ),
                align_items="center",
            ),
            justify_content="space-between",
            align_items="center",
        ),
        backdrop_filter="auto",
        backdrop_blur="lg",
        padding="12px",
        border_bottom=f"5px solid {rx.color('slate', 8)}",
        background_color=rx.color("slate", 10),
        position="sticky",
        top="0",
        z_index="100",
        align_items="center",
    )
