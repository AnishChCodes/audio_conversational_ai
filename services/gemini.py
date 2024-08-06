import google.generativeai as genai

from app_server.config import GEMINI_KEY


class Gemini:
    def __init__(self):
        from app import app

        app.logger.info("In Gemini")
        genai.configure(api_key=GEMINI_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        app.logger.info("Gemini initiated")

    def generate_text_content(self, prompt):
        from app import app

        app.logger.info(f"In generate_text_content - {prompt = }")
        response = self.model.generate_content(prompt)

        if response._done:
            return response.text.replace("*", "")
        raise Exception("Unable to answer the prompt")
