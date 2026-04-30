import json
import pandas as pd
import os
import math

JSON_PATH = '../web/feats_data.json'
EXCEL_PATH = '../web/traduccion_dotes.xlsx'

def import_from_excel():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, JSON_PATH)
    excel_path = os.path.join(script_dir, EXCEL_PATH)
    
    if not os.path.exists(excel_path):
        print(f"Error: No se encontró el archivo de Excel en {excel_path}")
        return
        
    print(f"Cargando Excel desde {excel_path}...")
    df = pd.read_excel(excel_path)
    
    print(f"Cargando JSON desde {json_path}...")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró feats_data.json.")
        return

    updated_count = 0
    
    for _, row in df.iterrows():
        item_id = str(row['ID'])
        name_es = row.get('Name (ES)', '')
        desc_es = row.get('Description (ES)', '')
        
        # Ignorar valores nulos o NaN de pandas
        if pd.isna(name_es):
            name_es = ""
        if pd.isna(desc_es):
            desc_es = ""
            
        if item_id in data:
            if 'es' not in data[item_id]:
                data[item_id]['es'] = {}
                
            data[item_id]['es']['name'] = str(name_es)
            data[item_id]['es']['description'] = str(desc_es)
            
            # Solo contar si realmente se tradujo algo
            if name_es or desc_es:
                updated_count += 1
                
    with open(json_path, 'w', encoding='utf-8') as out:
        json.dump(data, out, indent=4, ensure_ascii=False)
        
    print(f"Proceso completado. Se han integrado traducciones para {updated_count} dotes en el JSON.")
    print("La aplicación web ya reflejará estos cambios.")

if __name__ == "__main__":
    import_from_excel()
