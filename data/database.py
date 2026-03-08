from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://hungryorange@localhost:5432/motos_db')

df = pd.read_csv('data/motos.csv')
df.to_sql('motos', engine, if_exists='replace', index=False)

print(f"загружено {len(df)}")