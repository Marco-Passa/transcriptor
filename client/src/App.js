import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function App() {
  const [connected, setConnected] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [audioStream, setAudioStream] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  useEffect(() => {
    socket.on('connection_response', (data) => {
      console.log('Connected to backend');
      setConnected(true);
    });
    
    socket.on('transcription', (data) => {
      console.log('Audio transcripted');
      setTranscription(data.transcription);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const connectBackend = () => {
    socket.connect();
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorderInstance = new MediaRecorder(stream);
      mediaRecorderInstance.ondataavailable = handleDataAvailable;
      mediaRecorderInstance.start();
      setAudioStream(stream);
      setMediaRecorder(mediaRecorderInstance);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      audioStream.getTracks().forEach(track => track.stop());
    }
  };

  const handleDataAvailable = (event) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const audioData = reader.result.split(',')[1];
      socket.emit('audio_data', { audio: audioData });
    };
    reader.readAsDataURL(event.data);
  };



  return (
    <div>
      <button onClick={connectBackend}>Connect to Backend</button>
      {connected && (
        <div>
          <button onClick={startRecording}>Start Recording</button>
          <button onClick={stopRecording}>Stop Recording</button>
          <p>Transcription: {transcription}</p>
        </div>
      )}
    </div>
  );
}

export default App;