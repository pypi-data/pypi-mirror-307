import openai, time, os, base64
from dotenv import load_dotenv
from .prompts import uncensored_assistant, python_coder, rust_coder, summerizer, math, appunti

#caricara le variabili d'ambiente
load_dotenv()

url_mistral = 'https://api.mistral.ai/v1'
url_sambanova = 'https://api.sambanova.ai/v1'
url_openrouter = 'https://openrouter.ai/api/v1'
url_huggingface='https://api-inference.huggingface.co/v1/'
url_ollama='http://localhost:11434/v1'
url_github='https://models.inference.ai.azure.com'

img = False

#creazione degli agenti
class agente:
    def __init__(self, modello, prompt, url, nome, temperature):
        self.modello = modello
        self.prompt = prompt
        self.url = url
        self.nome = nome
        self.temperature = temperature
    
    def ottieni_dati(self):
        modello = self.modello
        prompt = self.prompt
        url = self.url
        nome = self.nome
        temperature = self.temperature
        return modello, prompt, url, nome, temperature

uncensored_assistant_1 = agente(modello='Meta-Llama-3.1-405B-Instruct', prompt=uncensored_assistant.system_prompt, url=url_sambanova, nome="Tank", temperature=0.8)
uncensored_assistant_2 = agente(modello='Llama-3.2-90B-Vision-Instruct', prompt=uncensored_assistant.system_prompt, url=url_sambanova, nome="Tank", temperature=0.8)
uncensored_assistant_3 = agente(modello='mistral-large-latest', prompt=uncensored_assistant.system_prompt, url=url_mistral, nome="Tank", temperature=0.8)
uncensored_assistant_4 = agente(modello='nousresearch/hermes-3-llama-3.1-405b:free', prompt=uncensored_assistant.system_prompt, url=url_openrouter, nome="Tank", temperature=0.8)
uncensored_assistant_5 = agente(modello='gpt-4o', prompt=uncensored_assistant.system_prompt, url=url_github, nome="Tank", temperature=0.8)

rust_coder_1 = agente(modello='codestral-latest', prompt=rust_coder.system_prompt, url=url_mistral, nome="Rusty", temperature=0.1)
rust_coder_2 = agente(modello='codestral-mamba-latest', prompt=rust_coder.system_prompt, url=url_mistral, nome="Rusty", temperature=0.1)
rust_coder_3 = agente(modello='nousresearch/hermes-3-llama-3.1-405b:free', prompt=rust_coder.system_prompt, url=url_openrouter, nome="Rusty", temperature=0.1)
python_coder_1 = agente(modello='codestral-latest', prompt=python_coder.system_prompt, url=url_mistral, nome="Pitone", temperature=0.1)
python_coder_2 = agente(modello='codestral-mamba-latest', prompt=python_coder.system_prompt, url=url_mistral, nome="Pitone", temperature=0.1)
python_coder_3 = agente(modello='nousresearch/hermes-3-llama-3.1-405b:free', prompt=python_coder.system_prompt, url=url_openrouter, nome="Pitone", temperature=0.1)

summerizer_1 = agente(modello='Meta-Llama-3.1-405B-Instruct', prompt=summerizer.system_prompt, url=url_sambanova, nome="Sam", temperature=0.4)
summerizer_2 = agente(modello='Llama-3.2-90B-Vision-Instruct', prompt=summerizer.system_prompt, url=url_sambanova, nome="Sam", temperature=0.4)
summerizer_3 = agente(modello='mistral-large-latest', prompt=summerizer.system_prompt, url=url_mistral, nome="Sam", temperature=0.4)
summerizer_4 = agente(modello='nousresearch/hermes-3-llama-3.1-405b:free', prompt=summerizer.system_prompt, url=url_openrouter, nome="Sam", temperature=0.4)
summerizer_5 = agente(modello='gpt-4o-mini', prompt=summerizer.system_prompt, url=url_github, nome="Sam", temperature=0.4)

math_1 = agente(modello='mathstral:latest', prompt="sei un'assistente utile, parla italiano e non formattare il testo in un altro formato", url=url_ollama, nome="Mat", temperature=0.1) #non serve dargli un prompt avanzato perché il modello è già istruito su quello che deve fare
math_2 = agente(modello='mistral-large-latest', prompt=math.system_prompt, url=url_mistral, nome="Mat", temperature=0.1)
math_3 = agente(modello='nousresearch/hermes-3-llama-3.1-405b:free', prompt=math.system_prompt, url=url_openrouter, nome="Mat", temperature=0.1)
math_4 = agente(modello='qwen/qwen-2-7b-instruct:free', prompt=math.system_prompt, url=url_openrouter, nome="Mat", temperature=0.1)

appunti_1 = agente(modello='Llama-3.2-90B-Vision-Instruct', prompt=appunti.system_prompt, url=url_sambanova, nome="Memo", temperature=0.6)
appunti_2 = agente(modello='meta-llama/llama-3.2-11b-vision-instruct:free', prompt=appunti.system_prompt, url=url_openrouter, nome="Memo", temperature=0.6)
appunti_3 = agente(modello='pixtral-12b-latest', prompt=appunti.system_prompt, url=url_mistral, nome="Memo", temperature=0.6)
appunti_4 = agente(modello='gpt-4o-mini', prompt=appunti.system_prompt, url=url_github, nome="Memo", temperature=0.6)

#funzioni principali
def seleziona_agente():
    global img
    while True:
        print("\033[95mSeleziona l'agente che desideri utilizzare:\n\033[0m\n\033[94m-----------------Chat Generica-----------------\033[0m\n1. Tank - Llama 3.1 405B uncensored (sambanova)\n2. Tank - Llama 3.2 90B uncensored (sambanova)\n3. Tank - Mistral large uncensored (mistral)\n4. Tank - Hermes 3 405 uncensored (openrouter)\n5. Tank - GPT 4o uncensored (github)\n\033[94m\n-----------------Programmazione----------------\033[0m\n6. Rusty - Codestral (mistral)\n7. Rusty - Codestral Mamba (mistral)\n8. Rusty - Hermes 3 405B (openrouter)\n9. Pitone - Codestral (mistral)\n10. Pitone - Codestral Mamba (mistral)\n11. Pitone - Hermes 3 405B (openrouter)\n\033[94m\n-------------------Riassunti-------------------\033[0m\n12. Sam - Llama 3.1 405B (sambanova)\n13. Sam - Llama 3.2 90B (sambanova)\n14. Sam - Mistral large (mistral)\n15. Sam - Hermes 3 405B (openrouter)\n16. Sam - GPT 4o mini (github)\n\033[94m\n------------------Matematica-------------------\033[0m\n17. Mat - Mathstral 7B (ollama)\n18. Mat - Mistral Large (mistral)\n19. Mat - Hermes 3 405B (openrouter)\n20. Mat - Qwen 2 7B (openrouter)\n\033[94m\n--------------------Appunti--------------------\033[0m\n21. Memo - Llama 3.2 Vision 90B (sambanova)\n22. Memo - Llama 3.2 Vision 11B (openrouter)\n23. Memo - Pixtral 12B (mistral)\n24. Memo - GPT 4o mini (github)\n")
        print("\033[91mAssicurati di avere almeno una delle chiavi api di sambanova, mistral, openrouter e/o github models nelle proprie variabile d'ambiente come SAMBANOVA_API_KEY, MISTRAL_API_KEY, OPENROUTER_API_KEY e GITHUB_API_KEY rispettivamente.\nNB: per usare i modelli ollama devi prima scaricarlo sul computer e poi scaricare localmente i modelli.\033[0m")
        print("\033[94m\nDigita '/exit' per uscire.\033[0m")
        scelta = input("\nInput:")
        #confronta la scelta con gli agenti, e quando trova quello corrispondente ne estrae i dati
        match scelta:
            case "1":
                img = False
                return uncensored_assistant_1.ottieni_dati()
            case "2":
                img = False
                return uncensored_assistant_2.ottieni_dati()
            case "3":
                img = False
                return uncensored_assistant_3.ottieni_dati()
            case "4":
                img = False
                return uncensored_assistant_4.ottieni_dati()
            case "5":
                img = False
                return uncensored_assistant_5.ottieni_dati()
            case "6":
                img = False
                return rust_coder_1.ottieni_dati()
            case "7":
                img = False
                return rust_coder_2.ottieni_dati()
            case "8":
                img = False
                return rust_coder_3.ottieni_dati()
            case "9":
                img = False
                return python_coder_1.ottieni_dati()
            case "10":
                img = False
                return python_coder_2.ottieni_dati()
            case "11":
                img = False
                return python_coder_3.ottieni_dati()
            case "12":
                img = False
                return summerizer_1.ottieni_dati()
            case "13":
                img = False
                return summerizer_2.ottieni_dati()
            case "14":
                img = False
                return summerizer_3.ottieni_dati()
            case "15":
                img = False
                return summerizer_4.ottieni_dati()
            case "16":
                img = False
                return summerizer_5.ottieni_dati()
            case "17":
                img = False
                return math_1.ottieni_dati()
            case "18":
                img = False
                return math_2.ottieni_dati()
            case "19":
                img = False
                return math_3.ottieni_dati()
            case "20":
                img = False
                return math_4.ottieni_dati()
            case "21":
                img = True
                return appunti_1.ottieni_dati()
            case "22":
                img = True
                return appunti_2.ottieni_dati()
            case "23":
                img = True
                return appunti_3.ottieni_dati()
            case "24":
                img = True
                return appunti_4.ottieni_dati()
            case "/exit":
                print("\033[95m\nArrivederci!\n\033[0m")
                exit(0)
            case _:
                print("\033[91mOpzione non valida, riprova.\033[0m")
                time.sleep(1)
                pulisci_schermo()

def converazione(client, modello, prompt, nome, temperature):
    global img
    pulisci_schermo()
    print(f"\033[95mSono {nome}, il tuo assistente personale, dimmi cosa posso fare per te.\033[0m \n") 

    time.sleep(1)
    while True:
        #chat
        try:
            domanda = input("\033[92m>\033[0m ")
        except UnicodeDecodeError:
            print("\033[91mInput non valido, riprova.\033[0m")
            time.sleep(1)


        if domanda == "/exit":
            break
        if "/file" in domanda and img == False:
            file = domanda.split(" ")[1]
            testo = leggi_doc(file)
            if testo:
                prompt += "file caricato:" + testo + "\n"
                print("\n\033[94m File caricato con successo\033[0m\n")
        if "/file" in domanda and img == True:
            file = domanda.split(" ")[1]
            base64_image = encode_image(file)

        if img == False:
            #invia l'input al client e restituisce la risposta
            risposta = client.chat.completions.create(
                model = modello,
                messages=[{"role":"system","content":prompt},{"role":"user","content":domanda}],
                temperature =  temperature,
                top_p = 0.1
            )

            print("\n\033[94m" + risposta.choices[0].message.content + "\033[0m\n")
        elif img == True:
            risposta = client.chat.completions.create(
                model=modello,
                messages=[
                    {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": domanda + "Trascrivi il testo contenuto in questa immagine"
                        #"text": "describe this image"
                        },
                        {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/jpeg;base64,{base64_image}"
                        },
                        },
                    ],
                    }
                ],
                temperature =  temperature,
                top_p = 0.1,
            )    
            print("\n\033[94m" + risposta.choices[0].message.content + "\033[0m\n")

        if modello != "mathstral:latest":
            #aggiunge la domanda e la risposta al contesto del prompt per la memoria dell'agente
            prompt += domanda + risposta.choices[0].message.content
        time.sleep(0.5)


def pulisci_schermo():
    comando = 'cls' if os.name == 'nt' else 'clear'
    os.system(comando)

def leggi_doc(path):
    try:
        with open(path, 'r') as file:
            testo = file.read()
            return testo
    except FileNotFoundError:
        print(f"Errore: il file '{path}' non esiste.")
    except IOError:
        print(f"Errore: impossibile leggere il file '{path}'.")
    except UnicodeDecodeError:
        print(f"Errore: il file '{path}' non è un file testo.")

def encode_image(image_path):
    try:
      with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Errore: il file '{image_path}' non esiste.")
    except IOError:
        print(f"Errore: impossibile leggere il file '{image_path}'.")

def main():
    while True:
        pulisci_schermo()
        modello, prompt, url, nome, temperature = seleziona_agente()
        if url == url_mistral:
            api_key = os.getenv("MISTRAL_API_KEY")
        elif url == url_sambanova:
            api_key = os.getenv("SAMBANOVA_API_KEY")
        elif url == url_openrouter:
            api_key = os.getenv("OPENROUTER_API_KEY")
        elif url == url_huggingface:
            api_key = os.getenv("HUGGINGFACE_API_KEY")
        elif url == url_ollama:
            api_key = "ollama"
        elif url == url_github:
            api_key = os.getenv("GITHUB_API_KEY")
        
        #crea un client e si connette all'api di sambanova o mistral
        client = openai.OpenAI(
            api_key=api_key,
            base_url=url,
        )

        converazione(client, modello, prompt, nome, temperature)



if __name__ == "__main__":
    main()
