import json
import urllib.request
import urllib.parse
import time
import os

def translate_text(text):
    if not text:
        return ""
    
    retries = 3
    for attempt in range(retries):
        try:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q=" + urllib.parse.quote(str(text))
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode('utf-8'))
            translated = "".join([x[0] for x in result[0]])
            
            # Fix HTML
            translated = translated.replace("< p >", "<p>").replace("< / p >", "</p>")
            translated = translated.replace("< strong >", "<strong>").replace("< / strong >", "</strong>")
            translated = translated.replace("< em >", "<em>").replace("< / em >", "</em>")
            
            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            time.sleep(2)
            
    return text

def main():
    en_json_path = os.path.join("..", "GitVTT", "pf2e-14-dev", "static", "lang", "en.json")
    out_path = os.path.join("..", "web", "traits_data.json")
    
    print(f"Leyendo {en_json_path}...")
    with open(en_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    pf2e_data = data.get("PF2E", {})
    
    # Extract trait names
    traits = {}
    for key, value in pf2e_data.items():
        if key.startswith("Trait") and not key.startswith("TraitDescription"):
            trait_id = key.replace("Trait", "").lower()
            if not trait_id:
                continue
            traits[trait_id] = {
                "en": {
                    "name": value,
                    "description": ""
                },
                "es": {
                    "name": "",
                    "description": ""
                }
            }
            
    # Extract descriptions
    for key, value in pf2e_data.items():
        if key.startswith("TraitDescription"):
            trait_id = key.replace("TraitDescription", "").lower()
            if trait_id in traits:
                traits[trait_id]["en"]["description"] = value
                
    total = len(traits)
    print(f"Encontrados {total} rasgos. Guardando resultados en {out_path}...")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(traits, f, ensure_ascii=False, indent=2)
        
    print("¡Listo!")

if __name__ == "__main__":
    main()
