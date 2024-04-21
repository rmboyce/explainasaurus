import reflex as rx
from website.state import State

# react-pdf library
class PdfLib(rx.Component):
    library = "react-pdf"
    def _get_custom_code(self) -> str:
        return """
        import { pdfjs } from "react-pdf";\n
        import "react-pdf/dist/esm/Page/TextLayer.css";\n
        import "react-pdf/dist/esm/Page/AnnotationLayer.css";\n
        pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;
        """

class PdfDocument(PdfLib):
    tag = "Document"
    file: rx.Var[str]
    def get_event_triggers(self) -> dict[str, rx.Var]:
        """Dict mapping (event -> expected arguments)."""

        return {
            **super().get_event_triggers(),
            "on_load_success": lambda e0: [rx.Var.create("_e0?.numPages", _var_is_local=False)],
        }

class PdfPage(PdfLib):
    tag = "Page"
    page_number: rx.Var[int]
    width: rx.Var[int]

document = PdfDocument.create
page = PdfPage.create

class SizeMe(rx.Component):
    library = "react-sizeme"
    tag = "SizeMe"


pdf_upload_color = "rgb(107,99,246)"


def pdf_upload():
    """The main view."""
    return rx.cond(
        State.uploaded,
        rx.vstack(
            rx.center(
                rx.heading(State.pdf),
                width="100%",
                padding="1em"
            ),
            document(
                rx.foreach(
                    State.get_page_numbers,
                    lambda i: page(page_number=i, width=1200)
                ),
                file=rx.get_upload_url(State.pdf),
                on_load_success=State.set_num_pages
            ),
            id="pdfParent"
        ),
        rx.box(
            rx.upload(
                rx.center(
                    #rx.button("Select File"),
                    rx.text("Drag and drop files here or click to select files!"),
                ),
                id="upload",
                accept = {
                    "application/pdf": [".pdf"]
                },
                disabled=False,
                on_keyboard=True,
                on_drop=State.handle_upload(rx.upload_files(upload_id="upload")),
                border=f"1px dotted {pdf_upload_color}",
                padding="3em"
            ),
            padding="3em"
        )
    )