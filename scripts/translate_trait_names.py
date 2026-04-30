import json
import urllib.request
import urllib.parse
import time
import os
import concurrent.futures

def translate_word(text):
    if not text: return ""
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q=" + urllib.parse.quote(str(text))
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        return "".join([x[0] for x in result[0]])
    except Exception:
        return text

def process_trait(item):
    trait_id, data = item
    if not data["es"]["name"] and data["en"]["name"]:
        data["es"]["name"] = translate_word(data["en"]["name"]).title()
    return trait_id, data

def main():
    path = os.path.join("..", "web", "traits_data.json")
    with open(path, 'r', encoding='utf-8') as f:
        traits = json.load(f)
        
    items = list(traits.items())
    print(f"Traduciendo {len(items)} nombres de rasgos de forma concurrente...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_trait, items))
        
    for trait_id, data in results:
        traits[trait_id] = data
        
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(traits, f, ensure_ascii=False, indent=2)
    print("¡Nombres traducidos y guardados!")

if __name__ == "__main__":
    main()
