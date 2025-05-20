import ollama
import os
from dotenv import load_dotenv

load_dotenv()

ollamaServer = os.getenv("OLLAMA_SERVER_URL") or ""
model = os.getenv("OLLAMA_MODEL_ID") or ""

client = ollama.Client(ollamaServer)

while True:
    print("----------------------Prompt---------------------")
    prompt = input("How may I help you (input q for quit): ")

    if prompt == 'q':
        print("Thank you. Hope to see you again.\n")
        break

    print("\n** Thinking......... **\n")

    response = client.generate(model=model, prompt=prompt)

    print("Response from ollama: ")
    print(response.response)
    print("\n------------------END--------------------------")