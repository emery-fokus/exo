from groq import Groq

from dotenv import load_dotenv
import base64
import os


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.conversation_history = [
                {
                    "role": "system",
                    "content": self.read_file(file_path="./context.txt")
                }
            ]


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


    def get_conversation_history(self):
        return self.conversation_history[1: ]


    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
            "role": role,
            "content": content,
            }
        )


    def ask_llm(self, text_interaction):

        self.update_conversation_history(role="user", content=text_interaction)

        response = self.groq_client.chat.completions.create(
            messages=self.conversation_history,
            model="openai/gpt-oss-120b",
            include_reasoning=False,
        ).choices[0].message.content


        self.update_conversation_history(role="assistant", content=response)

        return response


    def ask_llm_with_image(self, text_interaction, image_file):

        b64_image = base64.b64encode(image_file.read()).decode("utf-8")
        mime_type = image_file.type or "image/jpeg"

        image_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": text_interaction or "Décris cette image."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{b64_image}"},
                },
            ],
        }

        response = self.groq_client.chat.completions.create(
            messages=self.conversation_history + [image_message],
            model="qwen/qwen3.8-27b",
        ).choices[0].message.content

        self.update_conversation_history(
            role="user", content=text_interaction or "[Image envoyée]"
        )
        self.update_conversation_history(role="assistant", content=response)

        return response





























