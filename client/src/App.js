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
      setTranscription(oldTranscription => oldTranscription + ' ' + data.transcription);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const connectBackend = () => {
    socket.connect();
  };

  const start = async () => {
    try {
      // Infinite loop that stops and restarts recording every 3 seconds
      while (true) {
        console.log('ciao1')
        console.log('ciao2')
        const recording = await startRecording();
        console.log('ciao3')
        await wait(); // Wait for 3 seconds
        console.log('ciao4')
        stopRecording(recording); // Stop recording
        console.log('ciao5')
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorderInstance = new MediaRecorder(stream);
      mediaRecorderInstance.ondataavailable = handleDataAvailable;
      setAudioStream(stream);
      setMediaRecorder(mediaRecorderInstance);

      // Start recording initially
      mediaRecorderInstance.start();

      return { stream, mediaRecorderInstance };
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = (recording) => {
    if (recording && recording.mediaRecorderInstance) {
      recording.mediaRecorderInstance.stop();
      recording.stream.getTracks().forEach(track => track.stop());
    }
  };

  // Define a function to wait for 3 seconds
  const wait = async () => {
    return new Promise(resolve => {
      setTimeout(resolve, 5000);
    });
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
          <button onClick={start}>Start Recording</button>
          <button onClick={stopRecording}>Stop Recording</button>
          <p>Transcription: {transcription}</p>
        </div>
      )}
    </div>
  );
}

export default App;
