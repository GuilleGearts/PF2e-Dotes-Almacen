import json
import pandas as pd
import os

JSON_PATH = '../web/feats_data.json'
EXCEL_PATH = '../web/traduccion_dotes.xlsx'

def export_to_excel():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, JSON_PATH)
    excel_path = os.path.join(script_dir, EXCEL_PATH)
    
    print(f"Cargando datos desde {json_path}...")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró feats_data.json. Ejecuta parser.py primero.")
        return

    records = []
    for item_id, feat in data.items():
        records.append({
            'ID': item_id,
            'Name (EN)': feat['en']['name'],
            'Description (EN)': feat['en']['description'],
            'Name (ES)': feat.get('es', {}).get('name', ''),
            'Description (ES)': feat.get('es', {}).get('description', '')
        })
        
    df = pd.DataFrame(records)
    
    print(f"Exportando {len(df)} dotes a Excel...")
    df.to_excel(excel_path, index=False)
    print(f"Archivo generado exitosamente en: {excel_path}")
    print("Por favor completa las columnas 'Name (ES)' y 'Description (ES)' y luego ejecuta import_from_excel.py")

if __name__ == "__main__":
    export_to_excel()
