import joblib
import numpy as np
import pandas as pd


model = joblib.load("random_forest.pkl")


input_data = pd.DataFrame(
    [[25, 60, 15, 1, 2, 30]],
    columns=['Temp', 'Humidity', 'Wind', 'Soil', 'Vegetation', 'Rainfall']
)


prediction = model.predict(input_data)


risk_map = {0: 'High', 1: 'Low', 2: 'Medium'}
print("Predicted Risk:", risk_map[prediction[0]])