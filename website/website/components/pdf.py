import reflex as rx

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

document = PdfDocument.create
page = PdfPage.create



class PdfState(rx.State):
    """The app state."""

    # The pdf to render.
    pdf: str

    # is there an uploaded pdf?
    uploaded: bool = False

    num_pages: int = 0

    display_pages: list[int] = [1, 2, 3]


    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            self.pdf = file.filename
            self.uploaded = True


pdf_upload_color = "rgb(107,99,246)"

def on_load_success(num_pages: int):
    PdfState.set_num_pages(num_pages)
    rx.console_log(PdfState.num_pages)
    return []
    

def pdf_upload():
    """The main view."""
    return rx.cond(
        PdfState.uploaded,
        rx.vstack(
            rx.text(PdfState.pdf),
            rx.text(PdfState.num_pages),
            document(
                rx.foreach(PdfState.display_pages, lambda i: page(page_number=i)),
                file=rx.get_upload_url(PdfState.pdf),
                on_load_success=on_load_success
            )
        ),
        rx.upload(
            rx.vstack(
                rx.button("Select File", color=pdf_upload_color, bg="white", border=f"1px solid {pdf_upload_color}"),
                rx.text("Drag and drop files here or click to select files"),
            ),
            id="upload2",
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
            on_drop=PdfState.handle_upload(rx.upload_files(upload_id="upload2")),
            border=f"1px dotted {pdf_upload_color}",
            padding="5em",
        ),
    )