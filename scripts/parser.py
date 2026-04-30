import os
import json
import re

# Ajustar a la ruta del workspace
PATH_TO_PACKS = '../GitVTT/pf2e-14-dev/packs/pf2e/feats' 
OUTPUT_FILE = '../web/feats_data.json'

def clean_foundry_text(text):
    if not isinstance(text, str):
        return text
        
    # Reemplazar [[/command]]{Texto} -> <strong>Texto</strong>
    text = re.sub(r'\[\[[^\]]+\]\]\{([^}]+)\}', r'<strong>\1</strong>', text)
    
    # Reemplazar @Tag[ruta.a.Item]{Texto} -> <strong>Texto</strong>
    text = re.sub(r'@\w+\[[^\]]+\]\{([^}]+)\}', r'<strong>\1</strong>', text)
    
    # Reemplazar @UUID[ruta.a.Item.Nombre] -> <strong>Nombre</strong>
    # Captura la última parte del UUID que suele ser el nombre del item
    text = re.sub(r'@UUID\[.*?(?:[A-Za-z0-9_-]+\.)+([A-Za-z0-9_ -]+)\]', r'<strong>\1</strong>', text)
    
    # Reemplazar @Check[skill|...] -> <strong>Skill check</strong>
    text = re.sub(r'@Check\[([^|\]]+)[^\]]*\]', lambda m: f"<strong>{m.group(1).title()} check</strong>", text)
    
    # Genérico para macros restantes: @Tag[Valor] -> <strong>Valor</strong>
    text = re.sub(r'@\w+\[([^\]]+)\]', r'<strong>\1</strong>', text)
    
    return text

def parse_feats():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    packs_path = os.path.join(script_dir, PATH_TO_PACKS)
    output_path = os.path.join(script_dir, OUTPUT_FILE)
    
    combined_data = {}
    total_processed = 0
    
    print(f"Buscando archivos en: {packs_path}")
    
    for root, dirs, files in os.walk(packs_path):
        for file in files:
            if file.endswith('.json'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Nos aseguramos de procesar sólo items tipo 'feat'
                        if data.get('type') != 'feat':
                            continue
                            
                        item_id = data.get('_id')
                        system = data.get('system', {})
                        
                        description_raw = system.get('description', {}).get('value', '')
                        description_cleaned = clean_foundry_text(description_raw)
                        
                        combined_data[item_id] = {
                            "level": system.get('level', {}).get('value', 0),
                            "category": system.get('category', ''),
                            "traits": system.get('traits', {}).get('value', []),
                            "rarity": system.get('traits', {}).get('rarity', 'common'),
                            "publication": system.get('publication', {}).get('title', ''),
                            "en": {
                                "name": data.get('name', 'Unknown'),
                                "description": description_cleaned
                            }
                        }
                        total_processed += 1
                except Exception as e:
                    print(f"Error procesando {file}: {e}")
    
    # Crear carpeta web si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(combined_data, out, indent=4, ensure_ascii=False)
        
    print(f"Proceso completado. Se combinaron {total_processed} dotes en {output_path}")

if __name__ == "__main__":
    parse_feats()
