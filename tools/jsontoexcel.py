import json
import pandas as pd
import os

# Funktion zum Konvertieren von JSON-Dateien in Excel
def json_to_excel(json_files, excel_file):
    data = {}

    # Jede JSON-Datei einlesen und Daten sammeln
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            filename = os.path.basename(json_file).split('.')[0]  # Dateiname ohne Erweiterung
            data[filename] = json_data

    # Keys sammeln (sie sind in allen Dateien gleich)
    all_keys = list(data[next(iter(data))].keys())

    # DataFrame erstellen
    df = pd.DataFrame(index=all_keys)

    # Werte in DataFrame einfügen
    for filename, json_data in data.items():
        df[filename] = pd.Series(json_data)

    # DataFrame in Excel-Datei speichern
    df.to_excel(excel_file, na_rep='')

# Beispielnutzung
json_files = ['f1_gpt35_2nd_3rd.json', 'f1_gpt4_2nd_3rd.json', 'f1_gemini_2nd_3rd.json', 'f1_llama_2nd_3rd.json']
excel_file = 'f1_all_models_2nd_3rd.xlsx'
json_to_excel(json_files, excel_file)
