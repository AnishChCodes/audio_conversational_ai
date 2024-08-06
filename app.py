from uuid import uuid4

from flask import request, Response, make_response, jsonify
from werkzeug.exceptions import BadRequest

from app_server.app_server import create_app_server
from app_server.auth_utils import token_required, get_token
from app_server.config import DEFAULT_PASSWORD, DEFAULT_USERNAME
from app_server.db_connection import db
from models.audio_file import QnA
from services.google_cloud import BlobStorage
from validators.qna_request import validate_file

app, celery = create_app_server()


@app.get('/')
def index():
    app.logger.info('This is an INFO message')
    app.logger.debug('This is a DEBUG message')
    app.logger.warning('This is a WARNING message')
    app.logger.error('This is an ERROR message')
    app.logger.critical('This is a CRITICAL message')
    return 'Hello, World!'


@app.post("/login")
def login():
    auth = request.json
    if auth and auth.get("username") == DEFAULT_USERNAME and auth.get("password") == DEFAULT_PASSWORD:
        return get_token(auth)
    return make_response('Could not Verify', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})


@app.post('/qna/question/audio')
@token_required
def process_question():
    from tasks.qna import generate_answer

    app.logger.info(f"In process_question")
    validate_file(request.files)
    audio_file = request.files['audio_file']
    filename = f"media/uploads/{str(uuid4())}.{audio_file.filename.split('.')[-1]}"
    audio_file.save(f'{filename}')

    file_url, gcs_uri = BlobStorage().upload_blob(filename)
    new_file = QnA(incoming_file_url=file_url, incoming_file_gsc_uri=gcs_uri)
    db.session.add(new_file)
    db.session.commit()

    generate_answer.delay(new_file.id)

    return jsonify({
        "success": True,
        "qna_id": new_file.id
    })


@app.get('/qna/answer/audio/<id>')
def download_audio(id):
    retrieved_file = db.session.query(QnA).get(id)
    response = {
        "answer_url": retrieved_file.outgoing_file_url,
        "state": retrieved_file.state.value
    }
    return jsonify(response)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables on first run
    app.run(debug=True)
