import pandas as pd

# Datei- und Blattnamen anpassen
excel_file = 'Prompts.xlsx'
sheet_name = 'Sheet1'  
output_file = 'prompts.json'

# Excel-Datei einlesen
df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)

# Alle Zelleninhalte auslesen
all_cells = df.values.flatten().tolist()

# Inhalt in eine Textdatei schreiben
with open(output_file, 'w', encoding='utf-8') as f:
    for cell in all_cells:
        f.write(str(cell) + '\n')

print(f"Der Inhalt aller Zellen wurde erfolgreich in die Datei '{output_file}' geschrieben.")
