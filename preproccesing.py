import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder

random.seed(42)


df = pd.read_csv("data/weather.csv")


df = df[['Temp_C', 'Rel Hum_%', 'Wind Speed_km/h']]
df.columns = ['Temp', 'Humidity', 'Wind']

soil_types = ['Sandy', 'Clay', 'Loamy']
df['Soil'] = [random.choice(soil_types) for _ in range(len(df))]

veg_types = ['Low', 'Medium', 'High']
df['Vegetation'] = [random.choice(veg_types) for _ in range(len(df))]


df['Rainfall'] = df['Humidity'] * 0.5


def get_risk(row):
    if row['Wind'] > 20 and row['Humidity'] < 50:
        return 'High'
    elif row['Wind'] > 10:
        return 'Medium'
    else:
        return 'Low'

df['Risk'] = df.apply(get_risk, axis=1)


le1 = LabelEncoder()
le2 = LabelEncoder()
le3 = LabelEncoder()

df['Soil'] = le1.fit_transform(df['Soil'])
df['Vegetation'] = le2.fit_transform(df['Vegetation'])
df['Risk'] = le3.fit_transform(df['Risk'])


print("\nSoil Encoding:", dict(zip(le1.classes_, le1.transform(le1.classes_))))
print("Vegetation Encoding:", dict(zip(le2.classes_, le2.transform(le2.classes_))))
print("Risk Encoding:", dict(zip(le3.classes_, le3.transform(le3.classes_))))


df.to_csv("data/final_dataset.csv", index=False)

print("\nDataset created successfully!")
print(df.head())
print("Shape:", df.shape)