from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import base64
import speech_recognition as sr
import io
import os
from pydub import AudioSegment
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins='*')

def transcribe_audio(audio_data):
    recognizer = sr.Recognizer()

    # Decode the base64 data
    decoded_data = base64.b64decode(audio_data)

    # Write the decoded data to a file
    with open("./audio.opus", "wb") as f:
        f.write(decoded_data)

    # Convert from opus to wav file
    os.system(f'ffmpeg -y -i "{"./audio.opus"}" -vn "{"./audio.wav"}"')

    try:
        with sr.AudioFile("./audio.wav") as source:
            audio_data = recognizer.listen(source)
        transcription = recognizer.recognize_google(audio_data, show_all=False)
        transcription2 = recognizer.recognize_google(audio_data, show_all=True)
        print(len(transcription2['alternative']))
        for i in range(len(transcription2['alternative'])):
            print(transcription2['alternative'][i])

        return transcription
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Error occurred in transcription: {0}".format(e)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connection_response', {'data': 'Connected'})

@socketio.on('audio_data')
def handle_audio_data(data):
    audio_data = data['audio']
    transcription = transcribe_audio(audio_data)
    emit('transcription', {'transcription': transcription})

if __name__ == '__main__':
    socketio.run(app, debug=True)
