import os
import reflex as rx
from fastapi import Request
from pydantic import BaseModel

history = []


# Define a Pydantic model for the request body
class Item(BaseModel):
    link: str
    selected: str
    response: str

async def api_test(item: Item):
    history.append({"link": item.link, "selected": item.selected, "response": item.response, "checked": False})
    return {"link": item.link, "selected": item.selected}

class State(rx.State):
    """The app state."""

    # history of explanations
    shistory : list[dict[str, str]]= []

    # new explanation
    expl = "Default expl"

    summary: str = ""

    relativearticles: str = ""

    def shistory_toggle_checked(self, index: int):
        self.shistory[index]["checked"] = not self.shistory[index]["checked"]

    def generate_summary(self):
        self.summary = "GENERATED"

    def generate_relativearticles(self):
        self.relativearticles = "GENERATED"

    @rx.var
    def shistory_none_checked(self) -> bool:
        return all([not hist["checked"] for hist in self.shistory])

    def set_hist(self):
        self.shistory = history

    def add_explanation(self):
        # rx.console_log("in stuff"+new_explanation)
        self.history.append(self.expl)
    
    ### PDF STATE ###
    # The pdf to render.
    pdf: str

    # is there an uploaded pdf?
    uploaded: bool = False

    # number of pages
    num_pages: int = 0

    # page width
    width: int


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

    def update_width(self, width):
        self.width = width
    
    @rx.var
    def get_page_numbers(self) -> list[int]:
        return [i+1 for i in range(self.num_pages)]
