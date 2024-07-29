import json
import os
from glob import glob
from collections import defaultdict
import pandas as pd
import re

# Extrahieren des Modellnamens aus dem Dateinamen
def extract_model_name(filename):
    base_name = os.path.splitext(filename)[0]
    return base_name.split('_')[1].upper()

# Lesen und Zusammenfassen der JSON-Daten
def read_and_aggregate_json_files(json_files):
    aggregated_data = defaultdict(dict)
    for file in json_files:
        model_name = extract_model_name(file)
        with open(file, 'r') as f:
            json_data = json.load(f)
            for key, value in json_data.items():
                aggregated_data[key][model_name] = value
    
    # Durchschnitt der Werte für jeden Key berechnen
    averaged_data = {key:(sum(values.values())/len(values)) for key, values in aggregated_data.items()}
    
    return aggregated_data, averaged_data

# Alle JSON-Dateien im aktuellen Verzeichnis finden, die "f1" im Namen haben
json_files = [file for file in glob("*.json") if "f1" in file]

# JSON-Daten einlesen und aggregieren
aggregated_data, averaged_data = read_and_aggregate_json_files(json_files)

# Keys nach Durchschnittswerten sortieren
sorted_keys = sorted(averaged_data.keys(), key=lambda k: averaged_data[k], reverse=True)

# DataFrame
data = []
for key in sorted_keys:
    row = [key, averaged_data[key]]
    for model in aggregated_data[key]:
        row.append(aggregated_data[key][model])
    data.append(row)

# Spaltennamen für den DataFrame erstellen
columns = ['Categories', 'Avarage F1-Scores'] + list({extract_model_name(file) for file in json_files})

# DataFrame erstellen
df = pd.DataFrame(data, columns=columns)

# DataFrame in eine Excel-Datei speichern
df.to_excel("sorted_models.xlsx", index=False, float_format="%.3f")

print("Die Excel-Datei wurde erfolgreich erstellt.")


