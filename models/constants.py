from enum import Enum


class QnAStates(Enum):
    AUDIO_RECEIVED = "AUDIO_RECEIVED"
    TRANSCRIBED = "TRANSCRIBED"
    FETCHED_ANSWER = "FETCHED_ANSWER"
    SPEECH_SYNTHESIS = "SPEECH_SYNTHESIS"
    ANSWER_READY = "ANSWER_READY"
    FAILED = "FAILED"
