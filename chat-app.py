import ollama

ollamaServer = "https://arabic-oct-glossary-recent.trycloudflare.com"

client = ollama.Client(ollamaServer)

model = "gemma3:1b"
prompt = "what is Python?"

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