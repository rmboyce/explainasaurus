import os
import reflex as rx
from fastapi import Request
from pydantic import BaseModel
import requests
import json

history = []

# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    pass #raise Exception("Please set OPENAI_API_KEY environment variable.")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": [],
}

API_KEY = "AIzaSyCQHLZBNZws5jvxIRP1oIEkAiVaVoiInoI"

# Define a Pydantic model for the request body
class Item(BaseModel):
    link: str
    selected: str
    response: str

async def api_test(item: Item):
    history.append({"link": item.link, "selected": item.selected, "response": item.response})
    return {"link": item.link, "selected": item.selected}

class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # history of explanations
    shistory : list[dict[str, str]]= []

    summarylist : list[str] = []

    # new explanation
    expl = "Default expl"

    summary: str = ""

    relativearticles: str = ""

    def change_summary(self, checked: bool, response: str):
        if(checked):
            self.summarylist.append(response)
        else:
            self.summarylist.remove(response)
        rx.console_log(self.summarylist)

    def generate_summary(self):
        self.summary = "thinking..."
        return
        summary_prompt = "You are a helpful AI assistant summarizing information about Alzheimer's disease. You will be provided with several text excerpts related to Alzheimer's. Your task is to combine the key points from these texts into a single, concise summary. The summary should be easy to understand and should not be longer than the combined length of the input texts. Do not include any special formatting like bold or italics in your response. Focus on presenting a clear and informative overview of the disease based on the provided information. Here are the input texts, they are seperated by a newline:\n"
        for summary in self.summarylist:
            summary_prompt += summary
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
        return
        article_prompt = "You are a helpful AI assistant summarizing information about Alzheimer's disease. You will be provided with several text excerpts related to Alzheimer's. Your task is to combine the key points from these texts and find 3 related articles about the subject. The articles should appear in a list with one newline between each of them. The format for the links should be: '[Article name]: [url]'. Do not include any special formatting like bold or italics in your response. Focus on on finding relevant and recent articles. Here are the input texts, they are seperated by a newline:\n"
        for summary in self.summarylist:
            article_prompt += summary
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
    def empty_list(self) -> bool:
        return (len(self.summarylist)==0)

    def set_hist(self):
        self.shistory = history

    def add_explanation(self):
        # rx.console_log("in stuff"+new_explanation)
        self.history.append(self.expl)

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        model = self.openai_process_question

        async for value in model(question):
            yield value

    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {
                "role": "system",
                "content": "You are a friendly chatbot named Reflex. Respond in markdown.",
            }
        ]
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        session = OpenAI().chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=messages,
            stream=True,
        )

        # Stream the results, yielding after every word.
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                answer_text = item.choices[0].delta.content
                # Ensure answer_text is not None before concatenation
                if answer_text is not None:
                    self.chats[self.current_chat][-1].answer += answer_text
                else:
                    # Handle the case where answer_text is None, perhaps log it or assign a default value
                    # For example, assigning an empty string if answer_text is None
                    answer_text = ""
                    self.chats[self.current_chat][-1].answer += answer_text
                self.chats = self.chats
                yield

        # Toggle the processing flag.
        self.processing = False

    
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
