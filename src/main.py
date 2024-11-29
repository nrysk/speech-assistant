import json
import os

import dotenv
import google.generativeai as genai
import rich.console
import speech_recognition as sr

recognizer = sr.Recognizer()

dotenv.load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
)
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction='Suggest the some next sentence. Use the JSON format given below. {"given": "I left home and", "sentences": ["walked home, the afternoon sun warm on my face.", "immediately regretted my decision."]}',
)

console = rich.console.Console()


def print_screen(status: str, recognized: str, sentences: list[str]):
    console.clear()
    console.print("Instructions:")
    console.print("\tPress 'r'     to reset the recognized text.")
    console.print("\t      'q'     to quit.")
    console.print("\t      'Enter' to record.")
    console.print()
    console.print("Status:")
    console.print(f"\t{status}")
    console.print()
    console.print("Recognized:")
    console.print(f"\t{recognized}")
    console.print()
    console.print("Candidates:")
    for sentence in sentences:
        console.print(f"\t{sentence}")


if __name__ == "__main__":
    recognized = ""
    sentences = []

    while True:
        # 入力待機
        print_screen(
            "Waiting for input...",
            recognized,
            sentences,
        )
        key = input()
        if key == "q":
            print_screen(
                "Quitting...",
                recognized,
                sentences,
            )
            break
        elif key == "r":
            recognized = ""
            sentences = []
            continue

        # 録音
        print_screen(
            "Recording...",
            recognized,
            sentences,
        )
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        # 認識
        print_screen(
            "Recognizing...",
            recognized,
            sentences,
        )
        try:
            recognized += recognizer.recognize_google(audio, language="ja-JP")
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print(f"Could not request results; {e}\n")
            continue

        # 生成
        print_screen(
            "Generating...",
            recognized,
            sentences,
        )
        response = model.generate_content(recognized)
        sente = json.loads(response.text[8:-5]).get("sentences", [])
