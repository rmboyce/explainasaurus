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
    on_load_success: rx.EventHandler[lambda e0: [e0]]

class PdfPage(PdfLib):
    tag = "Page"
    page_number: rx.Var[int]
    width: rx.Var[int]

document = PdfDocument.create
page = PdfPage.create



pdf_upload_color = "rgb(107,99,246)"

'''
def on_load_success(num_pages: int):
    State.set_num_pages(num_pages)
    rx.console_log(State.num_pages)
    rx.call_script(
        "document.getElementById('pdfParent').offsetWidth",
        callback=State.update_width,
    ),
    return []'''


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
                    State.display_pages,
                    lambda i: page(page_number=i, width=1200)
                ),
                file=rx.get_upload_url(State.pdf),
                #on_load_success=State.set_num_pages
            ),
            id="pdfParent"
        ),
        rx.upload(
            rx.vstack(
                rx.button("Select File"),
                rx.text("Drag and drop files here or click to select files"),
            ),
            id="upload",
            accept = {
                "application/pdf": [".pdf"],
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
                "image/gif": [".gif"],
                "image/webp": [".webp"],
                "text/html": [".html", ".htm"],
            },
            disabled=False,
            on_keyboard=True,
            on_drop=State.handle_upload(rx.upload_files(upload_id="upload")),
            border=f"1px dotted {pdf_upload_color}",
            padding="5em",
            margin="5em"
        ),
    )