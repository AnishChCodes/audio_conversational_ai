from app import celery, app
from app_server.db_connection import db
from models.audio_file import QnA
from models.constants import QnAStates
from services.gemini import Gemini
from services.google_cloud import BlobStorage
from services.stt import SpeechRecogniser
from services.tts import TTS


@celery.task
def generate_answer(file_id):
    with app.app_context():
        app.logger.info("In generate_answer")
        retrieved_file = db.session.query(QnA).get(file_id)

        try:
            transcript = SpeechRecogniser().get_transcript(retrieved_file.incoming_file_gsc_uri)
            retrieved_file.incoming_text = transcript
            retrieved_file.state = QnAStates.TRANSCRIBED.value
            db.session.add(retrieved_file)
            db.session.commit()

            answer = Gemini().generate_text_content(transcript)
            retrieved_file.outgoing_text = answer
            retrieved_file.state = QnAStates.FETCHED_ANSWER.value
            db.session.add(retrieved_file)
            db.session.commit()

            answer_audio = TTS().generate_speech(answer)
            retrieved_file.state = QnAStates.SPEECH_SYNTHESIS.value
            db.session.add(retrieved_file)
            db.session.commit()

            file_url, gcs_uri = BlobStorage().upload_blob(answer_audio)
            retrieved_file.outgoing_file_url = file_url
            retrieved_file.state = QnAStates.ANSWER_READY.value
            db.session.add(retrieved_file)
            db.session.commit()
        except Exception as exc:
            app.logger.exception(exc)
            retrieved_file.reason = str(exc)
            db.session.add(retrieved_file)
            db.session.commit()
