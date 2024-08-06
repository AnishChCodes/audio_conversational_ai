from google.cloud import speech

from app_server.config import SPEECH_JSON


class SpeechRecogniser:
    def __init__(self):
        from app import app

        app.logger.info("In SpeechRecogniser")
        self.client = speech.SpeechClient.from_service_account_json(SPEECH_JSON)

    def get_transcript(self, gcs_uri):
        from app import app

        app.logger.info(f"In get_transcript {gcs_uri = }")
        audio = speech.RecognitionAudio(uri=gcs_uri)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            language_code="en-US",
        )

        response = self.client.recognize(config=config, audio=audio)
        transcript = ""
        for result in response.results:
            transcript += f" {result.alternatives[0].transcript} "

        app.logger.info(f"{transcript = }")
        return transcript
