import speech_recognition as sr
import base64
from pydub import AudioSegment

audio_data = "GkXfo59ChoEBQveBAULygQRC84EIQoKEd2VibUKHgQRChYECGFOAZwH/////////FUmpZpkq17GDD0JATYCGQ2hyb21lV0GGQ2hyb21lFlSua7+uvdeBAXPFh2MCFPg86LCDgQKGhkFfT1BVU2Oik09wdXNIZWFkAQEAAIC7AAAAAADhjbWERzuAAJ+BAWJkgSAfQ7Z1Af/////////ngQCjRDaBAACA+4P8OvwKf/yCLDaBtVJ8xcCvtv/1N/R7W7JquVqwz6f0f4myCK6NbOG4kDS3Daj3Qv/HIVxZLpajIiUA/m593V14rUNSV1pG7EorKCy8szf5+ajO6TXRrB21PZEt8lkpusqM1aZAcasnh01l94SA3BPsp7anslZuU9npt6XFTfSB9kL5pREFh0ycOxpZV46/rBpGEKqje+/+mg8hqwLt8U6dSMKG9XKS+bLDOxgQxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATz3G18TKVHm+CNKfPWdJgdI4aNRyNgDmhVuMhIk2W1c+Wyhd88kcgvmFtY6BoFMhYNLxhIyTwmm9ccuJgDhmIGFfqY67OfLvCxYhygQedbhquNlAEN6VIXC3o2HVspFgSC0OciSDVFR5kWEBpPwv0+nWYQMO6yY+bFRYdAPX/j93L59cufY20nFPBQvH8+ltM4AfYAF6blb6vx8ymbTwgy6nfcRd5e0Afob+kexWSZibfWVjKCcxUbr1zGwBYd94+DoF8Xyds4oVs9oym2RZo5V+mlk0xKV7EvAMQqHsjOyGkp3kzlORWjUBKfMKT8R6MSsuZg42cYgYVdH4SV98XfsPN9TqLdirmPtm+l4G/M1d5M7qvADwNhJhCkTSypDk+nBzjXRP9qGg+JlWnooA3znBE86WYOZd8B4MagcDG8pkTZ52RmzjElvKdRjD9bgxT3/2gnCzITENCCHEJFA9JM++JcKOm449kNnDX/+yKAVHbZnJ5iKH3GpnJ2kVDdph0tY6zTOY6ErzhZOSlGBW61oxwAMyyX2TpnTRn6JNjFjF6e4L2my8x/ZOAEWhBmBd4MdCUq5aKs57fk8eiEGkVGKa3pfH2ajANGQEwYsZPWSdl1Lr/GkG3GmNtIFr+YIVDv8+LD2+znKnostkHxjuEN1kjctvUAQmVI9yRJqZMeyZfcQ8zEA46u8vIUQHv++XQ/JNQR6f6yEpfZ8z2Y4HYWJE+CQl8bIuxWzuG9wNT7H52rRIAb7+wl8+KB44r5BkHd14mLKxFukIEGefxemoyh0tpAl1GXvGSA5o0rMODuITOVDLQSEJOFLEbwJsZUfcqdr+YVfroagu+dVyCi6fdvqCIvgZXB4PT3RAPXmSctugJRUIgmmLL7UAiJPz0f3eY5/Y"

def transcribe_audio(audio_data):
    recognizer = sr.Recognizer()

    # Decode the base64 data
    decoded_data = base64.b64decode(audio_data)

    # Load Opus audio using Pydub
    audio = AudioSegment.from_file_bytes(decoded_data)

    # Export as WAV (Google Speech-to-Text prefers WAV)
    audio.export("temp.wav", format="wav")

    # Load the WAV file
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)

    try:
        transcription = recognizer.recognize_google(audio_data, show_all=False)
        return transcription
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Error occurred in transcription: {0}".format(e)

print(transcribe_audio(audio_data))