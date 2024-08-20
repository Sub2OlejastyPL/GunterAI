import json
import pyttsx3 as pytt3
import speech_recognition as sr
import setuptools
from difflib import get_close_matches
from typing import Optional

recognizer = sr.Recognizer()

engine = pytt3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)



def load_knowledge(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_knowledge(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_matches(user_question: str, questions: list[str]) -> Optional[str]:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answ(question: str, knowledge_base: dict) -> Optional[str]:
    for q in knowledge_base.get("questions", []):
        if q["question"] == question:
            return q["answer"]
    return None


def chat():
    knowledge_base: dict = load_knowledge('ChatAI/knowledge.json')

    while True:
        user_input = ''
        try:
            print("\rTy: słuchanie...", end='')
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                # Using Google recognizer instead of Google Cloud
                rtext = recognizer.recognize_google(audio, language="pl-PL")
                rtext = rtext.capitalize()
                user_input = rtext  # Przypisanie do user_input

            print("\rTy: " + rtext)

        except sr.RequestError as e:
            print(f"Błąd połączenia z serwerem rozpoznawania mowy: {e}")
            user_input: str = input("Ty: ")
            continue  # Kontynuacja pętli zamiast return

        except sr.UnknownValueError:
            print("Nie można rozpoznać mowy")
            user_input: str = input("Ty: ")
            continue  # Kontynuacja pętli zamiast return

        if user_input.lower() == "quit":
            break

        best_match: Optional[str] = find_matches(user_input,
                                                 [q["question"] for q in knowledge_base.get("questions", [])])

        if best_match:
            answer: Optional[str] = get_answ(best_match, knowledge_base)
            if answer:
                print(f"Gunter: {answer}")
                engine.say(answer)
                engine.runAndWait()
        else:
            not_in_base = "Nie rozumiem, co mogę na to odpowiedzieć?"
            print("Gunter: " + not_in_base)
            engine.say(not_in_base)
            engine.runAndWait()

            try:
                print("Co to oznacza?")
                print("\rTy: słuchanie...", end='')
                with sr.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    # Using Google recognizer instead of Google Cloud
                    rtext = recognizer.recognize_google(audio, language="pl-PL")
                    rtext = rtext.capitalize()

                print("\rTy: " + rtext)
                new_answer = rtext  # Przypisanie nowej odpowiedzi

            except sr.RequestError as e:
                print(f"Błąd połączenia z serwerem rozpoznawania mowy: {e}")
                print("Co to oznacza?")
                new_answer = input("Napisz co to oznacza lub napisz 'Pomiń': ")
                continue

            except sr.UnknownValueError:
                print("Nie można rozpoznać mowy")
                print("Co to oznacza?")
                new_answer = input("Napisz co to oznacza lub napisz 'Pomiń': ")
                continue

            if new_answer.lower() != "pomiń":
                smth_new = "Dziękuję! Dzięki tobie nauczyłem się czegoś nowego."
                knowledge_base.setdefault("questions", []).append({"question": user_input, "answer": new_answer})
                save_knowledge('ChatAI/knowledge.json', knowledge_base)
                print("Gunter: " + smth_new)
                engine.say(smth_new)
                engine.runAndWait()



if __name__ == '__main__':
    chat()