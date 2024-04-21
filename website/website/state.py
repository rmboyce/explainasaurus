import os
import reflex as rx
from fastapi import Request
from pydantic import BaseModel
import requests
import json

history = []

API_KEY = "AIzaSyCQHLZBNZws5jvxIRP1oIEkAiVaVoiInoI"

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
        self.summary = "thinking..."
        summary_prompt = "You are a helpful AI assistant summarizing information about Alzheimer's disease. You will be provided with several text excerpts related to Alzheimer's. Your task is to combine the key points from these texts into a single, concise summary. The summary should be easy to understand and should not be longer than the combined length of the input texts. Do not include any special formatting like bold or italics in your response. Focus on presenting a clear and informative overview of the disease based on the provided information. Here are the input texts, they are seperated by a newline:\n"
        for summary in self.shistory:
            if(summary["checked"]):
                summary_prompt += summary["response"]
                summary_prompt += "\n"
        url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key='+API_KEY
        headers = {'Content-Type': 'application/json'}
        data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': summary_prompt
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            rx.console_log(response_data)
            resp = response_data['candidates'][0]['content']['parts'][0]['text']
            self.summary = resp.encode('utf-8').decode('unicode-escape')
            rx.console_log(self.summary)
        else:
            print('Error:', response.status_code)

    def generate_relativearticles(self):
        self.relativearticles = "thinking..."
        article_prompt = "You are a helpful AI assistant summarizing information about Alzheimer's disease. You will be provided with several text excerpts related to Alzheimer's. Your task is to combine the key points from these texts and find 3 related articles about the subject. The articles should appear in a list with one newline between each of them. The format for the links should be: '[Article name]: [url]'. Do not include any special formatting like bold or italics in your response. Focus on on finding relevant and recent articles. Here are the input texts, they are seperated by a newline:\n"
        for summary in self.shistory:
            if(summary["checked"]):
                article_prompt += summary["response"]
                article_prompt += "\n"
        url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key='+API_KEY
        headers = {'Content-Type': 'application/json'}
        data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': article_prompt
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            rx.console_log(response_data)
            resp = response_data['candidates'][0]['content']['parts'][0]['text']
            self.relativearticles = resp.encode('utf-8').decode('unicode-escape')
            rx.console_log(self.summary)
        else:
            print('Error:', response.status_code)

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
