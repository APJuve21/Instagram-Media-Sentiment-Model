import pandas as pd
df = pd.read_csv('HKLand_Input.csv')
TERM = []
for terms in df['Name']:
    TERM.append(terms)