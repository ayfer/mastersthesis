import json
import os
from glob import glob
from collections import defaultdict
import re

# Funktion zum Extrahieren des Basisnamens aus dem Dateinamen (ohne Nummerierung und Erweiterung)
def extract_basename(filename):
    return re.sub(r'_\d+\.json$', '', filename)

# Funktion zum Lesen und Zusammenfassen der JSON-Daten
def read_and_aggregate_json_files(json_files):
    aggregated_data = defaultdict(list)

    for file in json_files:
        with open(file, 'r') as f:
            json_data = json.load(f)
            for key, value in json_data.items():
                aggregated_data[key].append(value)

    # Durchschnitt der Werte für jeden Key berechnen und auf 3 Nachkommastellen runden
    averaged_data = {key: round(sum(values)/len(values), 3) for key, values in aggregated_data.items()}

    return averaged_data

# Alle JSON-Dateien im aktuellen Verzeichnis finden, die "f1" im Namen haben
json_files = [file for file in glob("*.json") if "f1" in file]

# Dictionary für Dateien mit ähnlichen Basenamen
grouped_files = defaultdict(list)

# Dateien nach Basename gruppieren
for file in json_files:
    basename = extract_basename(file)
    grouped_files[basename].append(file)

# Überprüfung der Gruppierung
print("Dateien gruppiert nach Basename:")
for basename, files in grouped_files.items():
    print(f"{basename}: {files}")

# Für jede Gruppe von Dateien die Daten aggregieren und speichern
for basename, files in grouped_files.items():
    print(f"\nAggregiere Dateien für {basename}: {files}")
    averaged_data = read_and_aggregate_json_files(files)
    # Daten nach den Werten sortieren (absteigend)
    sorted_averaged_data = dict(sorted(averaged_data.items(), key=lambda item: item[1], reverse=True))
    output_filename = f"{basename}.json"
    with open(output_filename, 'w') as f:
        json.dump(sorted_averaged_data, f, indent=4)
    print(f"Erstellte Datei: {output_filename}")

print("\nDie zusammengefassten Dateien wurden erfolgreich erstellt.")
