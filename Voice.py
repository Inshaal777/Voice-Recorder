import speech_recognition as sr
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
import tempfile

# Function to recognize the voice
def recognize_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        command = recognizer.recognize_google(audio)
        print("You said: " + command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand your speech.")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

# Function to convert text to speech
def speak(text):
    tts = gTTS(text=text, lang='en')
    # Save the audio as a temporary MP3 file
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(temp_audio.name)
    temp_audio.close()

    # Load the MP3 file and play it using pydub
    audio = AudioSegment.from_mp3(temp_audio.name)
    play(audio)

    # Delete the temporary audio file
    os.remove(temp_audio.name)

# Main loop for voice assistant
while True:
    command = recognize_speech().lower()

    if "hello" in command:
        speak("Hello there!")
    elif "what's your name" in command:
        speak("I'm your voice assistant.")
    elif "exit" in command:
        speak("Goodbye!")
        break
