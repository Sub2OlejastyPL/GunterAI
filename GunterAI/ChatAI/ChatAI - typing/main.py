import json
from difflib import get_close_matches
from typing import Optional

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
    while True:
        knowledge_base: dict = load_knowledge('ChatAI/knowledge.json')

        user_input: str = input("Ty: ")

        if user_input.lower() == "quit":
            break

        best_match: Optional[str] = find_matches(user_input,
                                                     [q["question"] for q in knowledge_base.get("questions", [])])

        if best_match:
            answer: Optional[str] = get_answ(best_match, knowledge_base)
            if answer:
                print(f"Gunter: {answer}")

        else:
            not_in_base = "Nie rozumiem, co mogę na to odpowiedzieć?"
            print("Gunter: " + not_in_base)
            new_answer = input("Napisz co to oznacza lub napisz 'Pomiń': ")


            if new_answer.lower() != "pomiń":
                smth_new = "Dziękuję! Dzięki tobie nauczyłem się czegoś nowego."
                knowledge_base.setdefault("questions", []).append({"question": user_input, "answer": new_answer})
                save_knowledge('ChatAI/knowledge.json', knowledge_base)
                print("Gunter: " + smth_new)


if __name__ == '__main__':
    chat()