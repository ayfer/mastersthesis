import json
import argparse
import matplotlib.pyplot as plt
import os

def main(input_file, output_file):
    # JSON-Datei einlesen
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Daten aufbereiten und sortieren (aufsteigend)
    items = sorted(data.items(), key=lambda x: (x[1], x[0]))
    #items = sorted(data.items(), key=lambda x: x[1])
    keys = [item[0] for item in items]
    values = [item[1] for item in items]

    # Farben festlegen: dunkelblau für initial_prompt, hellblau für alle anderen
    colors = ['darkgrey' if key == 'initial_prompt' else 'lightgrey' for key in keys]

    # Balkendiagramm erstellen
    plt.figure(figsize=(10, 8))
    bars = plt.barh(keys, values, color=colors)

    # Werte an die Balken schreiben
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.3f}', va='center', ha='left')
    plt.xlim(0, max([bar.get_width() for bar in bars]) * 1.1)

    # Beschriftungen und Titel hinzufügen
    plt.xlabel('F1-Score')
    plt.ylabel('Categories')
    plt.title('GPT-3.5 Intent Recognition Performance')

    # Layout anpassen und Diagramm speichern
    plt.tight_layout()
    plt.savefig(output_file)
    #plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a bar chart from a JSON file.')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file.')
    parser.add_argument('output_file', type=str, help='Name of the output image file.')

    args = parser.parse_args()
    output_file_path = os.path.join(os.getcwd(), args.output_file)
    main(args.input_file, output_file_path)
