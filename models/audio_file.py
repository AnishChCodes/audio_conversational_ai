from flask_sqlalchemy import SQLAlchemy

from app_server.db_connection import db
from models.constants import QnAStates

class QnA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incoming_file_url = db.Column(db.String(255), unique=True, nullable=False)
    incoming_file_gsc_uri = db.Column(db.String(255), unique=True, nullable=False)
    outgoing_file_url = db.Column(db.String(255), unique=True, nullable=True)
    incoming_text = db.Column(db.Text, nullable=True)
    outgoing_text = db.Column(db.Text, nullable=True)
    state = db.Column(db.Enum(QnAStates), default=QnAStates.AUDIO_RECEIVED.value)
    reason = db.Column(db.Text, nullable=True)
