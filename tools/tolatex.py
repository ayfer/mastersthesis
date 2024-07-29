import pandas as pd

# Lesen der Excel-Datei
df = pd.read_excel('Book5.xlsx')

# Konvertieren in LaTeX
latex_code = df.to_latex(index=False)

# Speichern des LaTeX-Codes in einer Datei
with open('book5.tex', 'w') as f:
    f.write(latex_code)
