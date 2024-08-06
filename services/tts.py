from text_to_speech import save
from uuid import uuid4

from app import app


class TTS:
    def __init__(self):
        from app import app

        app.logger.info("In TTS")
        self.language = "en"
        app.logger.info("TTS initiated")

    def generate_speech(self, text):
        from app import app

        app.logger.info("In generate_speech")
        output_file = f"media/generated/{uuid4()}.mp3"
        save(text, self.language, file=output_file)
        app.logger.info(f"Audio {output_file = }")
        return output_file
